import sys
from os import path
from Bio import SeqIO
inFileName = sys.argv[1]
gene_name = sys.argv[2]

records = SeqIO.parse(inFileName,"fasta")
out_records=[]

for record in records:
    if record.id == gene_name:
        out_records.append(record)

if len(out_records) > 1:
    for i in range(len(out_records)):
        out_records[i].description = "copy_" + str(i+1) + " " +out_records[i].description

outFileName = path.splitext(path.basename(inFileName))[0] + "." + gene_name + ".fasta"

SeqIO.write(out_records,outFileName,"fasta")
