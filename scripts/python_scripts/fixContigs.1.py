#remove invalid characters from fasta id's/descriptions
#replace all non ACTG bases with N

from Bio import SeqIO
import sys


inFileName = sys.argv[1]

records = list(SeqIO.parse(inFileName,"fasta"))

for record in records:
    record.id = record.id.replace("|","_")
    record.description = record.description.replace("|","_")
    for i in range(len(record.seq)):
        base = record.seq[i]
        if base not in ["A","C","T","G"]:
            record.seq = record.seq[:i] + "N" + record.seq[i+1:]
SeqIO.write(records,inFileName,"fasta")
