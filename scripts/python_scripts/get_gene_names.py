#parses output from summarizeMFANNOT.7.3.py in the identify_mito_contigs_pipeline_v7

#find a contig in the file and output the gene names associated with it

import sys

inLine= sys.argv[1]
contig = sys.argv[2]

line = inLine.rstrip("\n").split("\t")

gene_names = line[3]
gene_names = gene_names.split(",")
outFileName = contig + ".gene_names.txt"

outFile = open(outFileName,"w")

for gene in gene_names:
    if gene != "None":
        outFile.write(gene + "\n")
outFile.close()

