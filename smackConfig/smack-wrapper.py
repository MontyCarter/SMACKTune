#!/usr/bin/python3

import subprocess
import sys
import os
import re
import traceback
import time

print("here")

###Use SAT to indicate expected result matches actual result,
###Use UNSAT to indicate they did not match
def get_result(instanceName, output):
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
  return 'SAT' if passed==expected else 'UNSAT'

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

def print_result(instanceName, output, runtime):
    try:
        result    = get_result(instanceName, output)
    except AttributeError as e:
        print("###" + output + "###", file=sys.stderr)
        traceback.print_exc()
    runlength = -1
    best_sol  = -1
    seed      = -1
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
    instanceName = sys.argv[1]
    cutoffTime = int(float(sys.argv[3]))
    addArgs = sys.argv[6:]
    addArgs = collectVerifierOptions(addArgs)
    print_result(*run(instanceName, cutoffTime, addArgs))

