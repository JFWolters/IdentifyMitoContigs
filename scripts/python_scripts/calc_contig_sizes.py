from Bio import SeqIO

from sys import argv

inFileName = argv[1]

gene_title = argv[2]

records = SeqIO.parse(inFileName,"fasta")

outFileName = gene_title + ".sizes.tab"

outFile = open(outFileName,"w")
outFile.write("Species\tGene\tSize\n")
for record in records:
    gene=record.id
    species=record.description
    size=len(record.seq)
    outFile.write(species + "\t" + gene + "\t" + str(size) + "\n")

outFile.close()
