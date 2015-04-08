import subprocess
import sys
import os
import re
import traceback
import time

def get_result(output):
  if re.search(r'[1-9]\d* time out|Z3 ran out of resources|z3 timed out', output):
    return 'TIMEOUT'
  elif re.search(r'[1-9]\d* verified, 0 errors?|no bugs', output):
    return 'SAT'
  elif re.search(r'0 verified, [1-9]\d* errors?|can fail', output):
    return 'UNSAT'
  else:
    return 'unknown'

def run(instanceName, timeLimit, addArgs):
    cmd = ['smackverify.py', instanceName]
    cmd += ['--time-limit', str(timeLimit)]
    cmd += ['-o', instanceName + '.bpl']
    cmd += addArgs
    start = time.time()
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err  = p.communicate()
    output = (out+err).decode('utf-8')
    return output, (time.time() - start)

def print_result(output, runtime):
    try:
        result    = get_result(output)
    except AttributeError as e:
        print("here2", file=sys.stderr)
        print("###" + output + "###", file=sys.stderr)
        traceback.print_exc()
    runlength = -1
    best_sol  = -1
    seed      = -1
    print("Result for ParamILS: %(result)s, %(runtime)f, %(runlength)d, %(best_sol)d, %(seed)d" % locals())
    print(output)

def collectVerifierOptions(addArgs):
    return addArgs

if __name__ == "__main__":
    instanceName = sys.argv[1]
    cutoffTime = int(float(sys.argv[3]))
    addArgs = sys.argv[6:]
    addArgs = collectVerifierOptions(addArgs)
    print_result(*run(instanceName, cutoffTime, addArgs))

