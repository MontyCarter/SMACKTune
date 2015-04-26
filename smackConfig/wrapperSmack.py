#!/usr/bin/python3

import subprocess
import sys
import os
import re
import traceback
import time


###Use SAT to indicate expected result matches actual result,
###Use UNSAT to indicate they did not match
def get_outcome(instanceName, output):
  #Get expected result
  expected = True
  if re.search(r'[fF]ail', instanceName) or re.search(r'[fF]alse', instanceName):
    expected = False
  #Get actual result
  passed = False
  if re.search(r'[1-9]\d* time out|Z3 ran out of resources|z3 timed out', output):
    return 'TIMEOUT'
  elif re.search(r'[1-9]\d* verified, 0 errors?|no bugs', output):
    passed = True
  elif re.search(r'0 verified, [1-9]\d* errors?|can fail', output):
    passed = False
  else:
    return 'unknown'
  #Return SAT if passed matched expected
  return 'CORRECT' if passed==expected else 'WRONG'

def run(instanceName, timeLimit, addArgs):
    cmd = ['smackverify.py', instanceName]
    cmd += ['--time-limit', str(timeLimit)]
    cmd += ['-o', instanceName + '.bpl']
    cmd += addArgs
    start = time.time()
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err  = p.communicate()
    output = (out+err).decode('utf-8')
    return instanceName, output, (time.time() - start)

def get_result(instanceName, output, runtime):
    try:
        result    = get_outcome(instanceName, output)
    except AttributeError as e:
        print("###" + output + "###", file=sys.stderr)
        traceback.print_exc()
    runlength = -1
    best_sol  = -1
    seed      = -1

    return output, result, runtime, runlength, best_sol, seed

def print_result(output, result, runtime, runlength, best_sol, seed):
    print("Result for ParamILS: %(result)s, %(runtime)f, %(runlength)d, %(best_sol)d, %(seed)d" % locals())
    print(output)
    #print(output, file=sys.stderr)
  

def collectVerifierOptions(addArgs):
  allArgs = list()
  verifierBoolSwitches = list()
  ctr = 0
  while ctr < len(addArgs):
    boolSwitch = re.match(r'-CORRAL__bool__(.*)', addArgs[ctr])
    if boolSwitch:
      if addArgs[ctr+1]=="1":
        verifierBoolSwitches.append("/" + boolSwitch.group(1))
      ctr += 1
    else:
      allArgs.append(addArgs[ctr])
    ctr += 1

  if len(verifierBoolSwitches)!=0:
    allArgs.append('--verifier-options=' + " ".join(verifierBoolSwitches))
  #print(allArgs, file=sys.stderr)
  return allArgs

if __name__ == "__main__":
    #Args:
    #    0 - script name
    #    1 - instance name (input full filename)
    #    2 - instance specific information (this is the <rest> from instance file (all columns after filename))
    #    3 - cutoff time (time limit)
    #    4 - cutoff length (??? - pass "-1" if this param doesn't make sense)
    #    5 - seed (??? probably doesn't apply to SMACK (maybe z3 can take seed?))
    # rest - All remaining params are the parameters being tried by paramils
    instanceName = sys.argv[1]
    cutoffTime = int(float(sys.argv[3]))
    #Get rest of args
    addArgs = sys.argv[6:]
    #generated nested args, for --verifier-options-"XXX"
    addArgs = collectVerifierOptions(addArgs)
    print_result(*get_result(*run(instanceName, cutoffTime, addArgs))) 

