#!/usr/bin/python3

import subprocess
import sys
import os
import re
import traceback
import time

###########################
### Result file functions
###########################

###Parses a ParamILS result file, returns the parameters in ParamILS format
def getResultFileParams(resultFilename):
    with open(resultFilename, 'r') as resultFile:
        rawArgs = re.search(r'Active parameters: (.*)', resultFile.read()).group(1)
    #Break in to individual args
    rawArgs = rawArgs.split(', ')
    #Add SMACK wrapper's expected "-" to the front
    rawArgs = ['-' + arg for arg in rawArgs]
    #Break arg and value into two pieces
    rawArgs = [smplArg for cmplxArg in rawArgs for smplArg in cmplxArg.split('=')]
    return rawArgs

###Parses a ParamILS result file, returns the cutoff time used for experiment
def getResultFileCutoffTime(resultFilename):
    with open(resultFilename, 'r') as resultFile:
        cutoff = re.search(r'.*cutoff (.*)', resultFile.read()).group(1)
    return int(float(cutoff))



#############################
### Smack execution functions
#############################

### A wrapper for runSmack - gets rid of useless paramils required return values
def callSmackWrapper(instanceName, timeout, addArgs):
    (output, result, runtime, runlength, best_sol, seed) = runSmack(instanceName, timeout, addArgs)
    #Drop unuseful values, and reorder for easy slicing
    return [instanceName, runtime, result, output]

### Runs SMACK
def runSmack(instanceName, timeLimit, addArgs):
    curTime = str(time.time())
    oFilename = instanceName + '_' + curTime + '.bpl'
    bcFilename = instanceName + '_' + curTime + '.bc'
    cmd =  ['smackverify.py', instanceName]
    cmd += ['--time-limit',   str(timeLimit)]
    cmd += ['-o',             oFilename]
    cmd += ['--bc',           bcFilename]
    cmd += addArgs
    start = time.time()
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err  = p.communicate()
    end = time.time()
    output = (out+err).decode('utf-8')
    runtime = end-start
    #print("\n",file=sys.stderr)
    #print(output,file=sys.stderr)
    #print("\n",file=sys.stderr)

    #Clean up bpl and bc files so we don't collect too many
    try:
      os.remove(oFilename)
    except:
      pass
    try:
      os.remove(bcFilename)
    except:
      pass

    return prepareSmackResult(instanceName, output, runtime)

###Parse output of SMACK to determine whether we got the right outcome
def getRunSmackOutcome(instanceName, smackOutput):
  #Get expected result
  expected = True
  if re.search(r'[fF]ail', instanceName) or re.search(r'[fF]alse', instanceName):
    expected = False
  #Get actual result
  passed = False
  if re.search(r'[1-9]\d* time out|Z3 ran out of resources|z3 timed out', smackOutput):
    return 'TIMEOUT'
  elif re.search(r'[1-9]\d* verified, 0 errors?|no bugs', smackOutput):
    passed = True
  elif re.search(r'0 verified, [1-9]\d* errors?|can fail', smackOutput):
    passed = False
  else:
    #return 'unknown'
    return 'WRONG'
  #Return SAT if passed matched expected
  return 'CORRECT' if passed==expected else 'WRONG'

###Returns all info needed regarding the run
def prepareSmackResult(instanceName, output, runtime):
    try:
        result    = getRunSmackOutcome(instanceName, output)
    except AttributeError as e:
        print("###" + output + "###", file=sys.stderr)
        traceback.print_exc()
    runlength = -1
    best_sol  = -1
    seed      = -1

    return [output, result, runtime, runlength, best_sol, seed]

 
### Takes parameter list in ParamILS format, collects all verifier options into
###    a single --verifier-options option
def collectVerifierOptions(addArgs):
  allArgs = list()
  verifierOptions = list()
  ctr = 0
  while ctr < len(addArgs):
    #If we match this regex, we're getting a nested param.  Take it apart, and reconstruct it
    #  appropriately
    #First group is destination, second group is type, third group is target nested parameter
    nestedArg = re.match(r'-(CORRAL|BOOGIE|Z3)(__bool__|__int__|__float__)(.*)', addArgs[ctr])
    if nestedArg:
      if nestedArg.group(1) == 'CORRAL':
        if nestedArg.group(2) == '__bool__':
          if addArgs[ctr+1] == '1':
            verifierOptions.append('/' + nestedArg.group(3))
        else:
          raise ("Unsupported Corral parameter type: " + nestedArg.group(2))

      if nestedArg.group(1) == 'BOOGIE':
        if nestedArg.group(2) == '__bool__':
          if addArgs[ctr+1] == '1':
            verifierOptions.append('/' + nestedArg.group(3))
        else:
          raise ("Unsupported Boogie parameter type: " + nestedArg.group(2))

      if nestedArg.group(1) == 'Z3':
        if nestedArg.group(2) == '__bool__':
          if (addArgs[ctr+1] == '1' or addArgs[ctr+1] == '0'):
            verifierOptions.append('/z3opt:' + nestedArg.group(3) + 
                                   "=" + ("true" if addArgs[ctr+1] == '1' else "false"))
          else:
            raise "Z3 __bool__ options must be either 0 or 1"
        elif nestedArg.group(2) == '__int__':
          verifierOptions.append('/z3opt:' + nestedArg.group(3) + '=' + addArgs[ctr+1])

        else:
          raise ("Unsupported Z3 parameter type: " + nestedArg.group(2))

      #Pull an extra param off the list, since we don't want this params value to remain on SMACK params
      ctr += 1
    else:
      allArgs.append(addArgs[ctr])
    ctr += 1

  if len(verifierOptions)!=0:
    allArgs.append('--verifier-options=' + " ".join(verifierOptions))
  #print("\n", file=sys.stderr)
  #print(allArgs, file=sys.stderr)
  #print("\n", file=sys.stderr)
  return allArgs



#############################
### Batch execution functions
#############################

###Runs smack on a list of files
def batchRunSmack(fileList, timeout, addArgs, showProgress=False):
    res = []
    cnt = 0
    lastlength = 0
    #Collect results from each benchmark
    for inFile in fileList:
        result = callSmackWrapper(inFile, timeout, addArgs)
        res.append(result)
        if showProgress:
            cnt += 1
            msg = str(cnt) + '/' + str(len(fileList)) + ' : ' + ' '.join(map(str,res[-1][:-1]))
            #Clear the line (in case last one was longer)
            print(' '*lastlength, end='\r')
            print(msg, end='\r')
            lastlength = len(msg)
    if showProgress:
        print(' '*lastlength, end='\r')
    return res

###Generates stats on a batch run
def getBatchStats(resultList):
    satCnt = unsatCnt = timeoutCnt = totalTime = 0
    for result in resultList:
        if result[2] == "CORRECT":
            satCnt += 1
        elif result[2] == "WRONG":
            unsatCnt += 1
        elif result[2] == "TIMEOUT":
            timeoutCnt += 1
        totalTime += result[1]
    return [satCnt, unsatCnt, timeoutCnt, totalTime]

###Formats stats from a batch run for printing
def formatBatchStatSummary(stats):
    (satCnt, unsatCnt, timeoutCnt, totalTime) = stats
    out =  "Summary:"
    out += "\n\tCORRECT Count:\t" + str(satCnt)
    out += "\n\tWRONG Count:\t" + str(unsatCnt)
    out += "\n\tTIMEOUT Count:\t" + str(timeoutCnt)
    out += "\n\tTotal Runtime:\t" + str(totalTime) + "\n"
    return out

###Formats a batch file for printing
def formatBatchFile(resultList, printSummary=False):
    toFile = []
    longestFile = longestFloat = 0
    for result in resultList:
        #track longest filename for printing alignment
        longestFile = longestFile if len(result[0])<=longestFile else len(result[0])
        longestFloat = longestFloat if len(str(result[1]))<=longestFloat else len(str(result[1]))

    for result in resultList:
        #Align printing
        #Convert from list of lists to list of output lines
        toFile.append(result[0] + " "*(longestFile-len(result[0])+1) + 
                      str(result[1]) + " "*(longestFloat-len(str(result[1]))+1) + 
                      result[2])

    ret = "\n".join(toFile)
    if printSummary:
        stats = getBatchStats(resultList)
        ret += formatBatchStatSummary(stats)
    return ret

###Writes a batch file (any string, really...)
def writeBatchFile(fileName, contents):
    with open(fileName, 'w') as instFile:
        instFile.write(contents)
