import sys

inSummaryLine = sys.argv[1]

inGeneNames = sys.argv[2]

inGenesFile = open(inGeneNames,"r")

inGenesLines = inGenesFile.readlines()

inGenesFile.close()

genes = [line.rstrip("\n") for line in inGenesLines]

summary_line = inSummaryLine.rstrip("\n").split("\t")
# print(summary_line)
#account for , delimited gene names
#converts gene names to a list at same index
gene_names = summary_line[3]
gene_names = gene_names.split(",")
summary_line[3] = gene_names

gene_count = int(summary_line[2])
for gene in genes:
    if gene in summary_line[3]:
        summary_line[3].remove(gene)
        gene_count -= 1

if len(summary_line[3]) < 1:
    summary_line[3] = ["None"]
    
    
summary_line[2] = str(gene_count)

out_line = summary_line[0] + "\t"
out_line = out_line + summary_line[1] + "\t"
out_line = out_line + summary_line[2] + "\t"
for gene_name in summary_line[3]:
    out_line = out_line + gene_name + ","
out_line = out_line.rstrip(",") + "\n"

sys.stdout.write(out_line)
