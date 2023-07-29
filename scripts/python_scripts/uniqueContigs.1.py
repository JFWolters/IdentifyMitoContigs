#outputs a file with no duplicate lines

import sys
import os

inFileName=sys.argv[1]

inFile = open(inFileName,"r")

lines = inFile.readlines()

inFile.close()

lines = set(lines)

outFileName = os.path.basename(inFileName)

outFileName = os.path.splitext(outFileName)[0] + ".unique.txt"

outFile = open(outFileName,"w")

for line in lines:
    outFile.write(line)

outFile.close()
