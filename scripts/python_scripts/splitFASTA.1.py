### Takes in a set of sequences in fasta format
### outputs each sequence in the file as a separate file

from Bio import SeqIO
import sys

seqFile = sys.argv[1]

records = SeqIO.parse(seqFile,"fasta")

for record in records:

    fn = record.id+".fasta"
    
    try:
        SeqIO.write(record,fn,"fasta")
    except FileNotFoundError:
        print("Error could not write file ",fn)