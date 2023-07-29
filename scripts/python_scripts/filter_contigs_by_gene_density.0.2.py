#V0.2 update
#fixed unintentional behavior in which contigs with 0 genes annotated were always excluded regardless of lengths


#V0.1 update
#Modified output to be lines from annotation_summary to better fit integration into whole pipeline
#output file name now based on input file name with no need to pass [species]

import sys

inFileName = sys.argv[1] #annotation summary file with contig lengths and gene count info

bp_amount = sys.argv[2] #Filtered contigs will have at least 1 gene per this # of bp

#e.g. a contig with 1 gene in 10,000 bp survives a 30kbp filter, but a contig with 2 genes in 250kbp will not.
density_cutoff = 1 / int(bp_amount)

inFile = open(inFileName,"r")

lines = inFile.readlines()

inFile.close()

tab_lines = [line.rstrip("\n").split("\t") for line in lines]
tab_lines.pop(0) #remove header
outFileName = inFileName.rstrip("tab") + "density_filtered." + bp_amount + ".tab"

outFile = open(outFileName,"w")

outFile.write(lines.pop(0)) #write the header, while removing it from lines

for i in range(len(lines)):
    
    contig = tab_lines[i][0]
    contig_length = int(tab_lines[i][1])
    gene_count = int(tab_lines[i][2])
    
    gene_density = gene_count / contig_length
    if gene_count == 0:
        if contig_length < int(bp_amount):
            outFile.write(lines[i])
    else:
        if gene_density > density_cutoff:
            outFile.write(lines[i])

outFile.close()

