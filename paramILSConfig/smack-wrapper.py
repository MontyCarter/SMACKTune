import subprocess
import sys
import os
import re

def get_result(output):
  if re.search(r'[1-9]\d* time out|Z3 ran out of resources|z3 timed out', output):
    return 'TIMEOUT'
  elif re.search(r'[1-9]\d* verified, 0 errors?|no bugs', output):
    return 'SAT'
  elif re.search(r'0 verified, [1-9]\d* errors?|can fail', output):
    return 'UNSAT'
  else:
    return 'unknown'

def get_runtime(output):
    totalTimeMatch = re.search(r'Total Time:\s*(\d\.\d+)\s*s\s*', output)
    return float(totalTimeMatch.group(1))
    
def run(instanceName, timeLimit):
    cmd = ['smackverify.py', instanceName]
    cmd += ['--time-limit', str(timeLimit)]
    cmd += ['-o', instanceName + '.bpl']
    #cmd += addArgs
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err  = p.communicate()
    output = out+err
    return output

def print_result(output):
    result    = get_result(output)
    runtime   = get_runtime(output)
    runlength = -1
    best_sol  = -1
    seed      = -1
    print("Result for ParamILS: %(result)s, %(runtime)f, %(runlength)d, %(best_sol)d, %(seed)d" % locals())
    print(output)


if __name__ == "__main__":
    instanceName = sys.argv[1]
    cutoffTime = int(float(sys.argv[3]))
    addArgs = sys.argv[6:]
    print_result(run(instanceName, cutoffTime))

