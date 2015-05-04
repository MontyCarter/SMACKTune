#!/usr/bin/python3

import sys
from helperSmack import *

def printResultForParamils(result):
    (output, outcome, runtime, runlength, best_sol, seed) = result
    #Print paramils result string
    print("Result for ParamILS: %(outcome)s, %(runtime)f, %(runlength)d, %(best_sol)d, %(seed)d" % locals())
    #Print smack output
    print(output)

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
    result = runSmack(instanceName, cutoffTime, addArgs)
    printResultForParamils(result)

