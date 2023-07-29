##Designed to run on output of Mfannot sqn file after conversion to genbank format with asn2gb
##Replaceds the "C_0" faulty locus definition with the correct record ID from the corresponding fasta
##Note the fasta is assumed to only have 1 sequence in it

import sys
from Bio import SeqIO
import os

inGbFileName = sys.argv[1]
inFastaFileName = sys.argv[2]

gbFile = open(inGbFileName,"r")

gbLines = gbFile.readlines()

gbFile.close()

# record = SeqIO.parse(inFastaFileName,"fasta").__next__()
record = list(SeqIO.parse(inFastaFileName,"fasta"))[0]

ID = record.id

out_lines = []
for line in gbLines:
    if line.startswith("LOCUS"):
        line = line.replace("C_0",ID)
    out_lines.append(line)

noPathInFileName = os.path.basename(inGbFileName)

baseInFileName , baseInFileExt = os.path.splitext(noPathInFileName)

outFileName = baseInFileName + ".locus_fixed.gb"

outFile = open(outFileName,"w")

for line in out_lines:
    outFile.write(line)
    
outFile.close()
