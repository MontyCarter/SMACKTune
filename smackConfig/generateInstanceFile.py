#!/usr/bin/python3

import sys
import glob
import os
from wrapperSmack import *

dfltTimeout = 120
dfltArgs = ['--unroll', '12']


def callSmackWrapper(instanceName):
    addArgs = dfltArgs
    output, result, runtime, runlength, best_sol, seed = get_result(*run(instanceName, dfltTimeout, addArgs))
    return [instanceName, runtime, result]

def genInstanceFile(folder):
    #Ensure trailing slash
    folder = folder if folder[-1] == "/" else folder + "/"
    res = []
    longestFile = longestFloat = satCnt = unsatCnt = timeoutCnt = totalTime = 0
    #Collect results from each benchmark
    for inFile in sorted(glob.glob(folder + "*.c")):
        res.append(callSmackWrapper(inFile))
        #track longest filename for printing alignment
        longestFile = longestFile if len(res[-1][0])<=longestFile else len(res[-1][0])
        longestFloat = longestFloat if len(str(res[-1][1]))<=longestFloat else len(str(res[-1][1]))
        if res[-1][2] == "CORRECT":
            satCnt += 1
        elif res[-1][2] == "WRONG":
            unsatCnt += 1
        elif res[-1][2] == "TIMEOUT":
            timeoutCnt += 1
        totalTime += res[-1][1]
        #print so we can see progress
        print(" ".join(map(str,res[-1])))

    #Convert from list of lists to list of output lines
    toFile = []
    for inst in res:
        #Align printing
        toFile.append(inst[0] + " "*(longestFile-len(inst[0])+1) + 
                      str(inst[1]) + " "*(longestFloat-len(str(inst[1]))+1) + 
                      inst[2])

    print("Summary:")
    print("\tCORRECT Count:\t" + str(satCnt))
    print("\tWRONG Count:\t" + str(unsatCnt))
    print("\tTIMEOUT Count:\t" + str(timeoutCnt))
    print("\tTotal Runtime:\t" + str(totalTime))

    return toFile

def writeInstanceFile(fileName, folder):
    with open(fileName, 'w') as instFile:
        instFile.write("\n".join(genInstanceFile(folder)))

writeInstanceFile('instanceSmack.txt', sys.argv[1])
