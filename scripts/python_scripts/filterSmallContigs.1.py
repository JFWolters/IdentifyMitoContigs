import sys

# from os import path

from Bio import SeqIO

inFileName = sys.argv[1]

size_cutoff = int(sys.argv[2])

records = SeqIO.parse(inFileName,"fasta")

out_records = []

for record in records:
    if len(record.seq) > size_cutoff:
        out_records.append(record)
        
# outFileName = path.splitext(path.basename(inFileName))[0] + ".fasta"
outFileName = inFileName

SeqIO.write(out_records,outFileName,"fasta")
