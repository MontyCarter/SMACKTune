#!/usr/bin/python3

import sys
import glob
import os
from wrapperSmack import *

dfltTimeout = 120
dfltArgs = ['--unroll', '12', '--verifier', 'boogie']

def getFileList(folder):
    #Ensure trailing slash
    folder = folder if folder[-1] == "/" else folder + "/"
    return sorted(glob.glob(folder + "*.c"))

def genInstanceFile(fileList, timeout=dfltTimeout, addArgs=dfltArgs):
    res = batchRunSmack(fileList, timeout, addArgs, showProgress=True)
    stats = getBatchStats(res)
    print(formatBatchStatSummary(stats))
    return formatBatchFile(res)

if __name__ == '__main__':
    folder = sys.argv[1]
    instanceList = getFileList(folder)
    instFileString = genInstanceFile(instanceList)
    writeBatchFile('instanceSmack.txt', instFileString)
