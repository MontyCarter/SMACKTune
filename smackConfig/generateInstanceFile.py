#!/usr/bin/python3

import sys
import glob
import os
from wrapperSmack import *

dfltTimeout = 30
dfltArgs = ['--unroll', '8']


def callSmackWrapper(instanceName):
    addArgs = dfltArgs
    output, result, runtime, runlength, best_sol, seed = get_result(*run(instanceName, dfltTimeout, addArgs))
    return [instanceName, str(runtime), result]

def genInstanceFile(folder):
    #Ensure trailing slash
    folder = folder if folder[-1] == "/" else folder + "/"
    res = []
    longestFile = 0
    longestFloat = 0
    for inFile in sorted(glob.glob(folder + "*.c")):
        res.append(callSmackWrapper(inFile))
        #track longest filename for printing alignment
        longestFile = longestFile if len(res[-1][0])<=longestFile else len(res[-1][0])
        longestFloat = longestFloat if len(res[-1][1])<=longestFloat else len(res[-1][1])
        #print so we can see progress
        print(" ".join(res[-1]))

    toFile = []
    for inst in res:
        #Align printing
        toFile.append(inst[0] + " "*(longestFile-len(inst[0])+1) + 
                      inst[1] + " "*(longestFloat-len(inst[1])+1) + 
                      inst[2])

    return toFile

def writeInstanceFile(fileName, folder):
    with open(fileName, 'w') as instFile:
        instFile.write("\n".join(genInstanceFile(folder)))

writeInstanceFile('instanceSmack.txt', sys.argv[1])
