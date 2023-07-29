###Read over the output from summarizeMFANNOT.1.py
###summarize the summary
###export results as one line appended into a specified file

##V3.3 update
#Now accounts for , delimited gene names in input


##V3.2 update
##Now takes species as input to avoid file naming issues if "." is in species (base file name for all outputs)


##V3.1 update
##added functionality to properly generate output file name even if input file name isn't in the same dir

##V3 update
##Now outputs as a separate file rather than adding to the main file
##Species is now inferred from summaryFileName which should start with [species].whatever

##V2 update
##Added functionality to determine whether given annotations appear multiple times
##and track this on a per contig basis
##Also only runs on output from summarizeMFANNOT.5.py (and presumably later versions) due to assembly length tracking now in summary file


import sys
import os

def processInputs():

    summaryFileName = sys.argv[1]
    
    geneFileName = sys.argv[2]
    
    species = sys.argv[3]
    
    return summaryFileName, geneFileName , species
    
def readSummaryFile(summaryFileName):

    summaryFile = open(summaryFileName,"r")
    
    lines = summaryFile.readlines()
    
    summaryFile.close()
    
    return lines
    
def processSummaryFile(lines):
    
    lines = [line.rstrip("\n") for line in lines]
    
    lines = [line.split("\t") for line in lines]
    
    lines.pop(0) #remove header line
    
    lines = [line for line in lines if len(line) > 2] #remove entries with no gene hits
    #note that the line above is redundant with the filtering already present in the script generating the summary file
    #It might be worth coming up with more consistent approach to filtering, do we filter here or in the prior script?
    
    contigs = []
    
    genes = []
    
    most_genes = 0
    
    genes_by_contig = []
    
    for line in lines:
    
        contig = line.pop(0)
        
        contigs.append(contig)
        
        contig_length = int(line.pop(0)) #required in output from summarizeMFANNOT.5.py (and presumably later versions)
        
        num_genes = int(line.pop(0))
        
        line = line[0].split(",") #split up the comma delimited gene names
        
        genes_by_contig.append(line)
        
        if num_genes > most_genes:
            most_genes = num_genes
        
        for gene in line:
        
            if "_" in gene: #treats multi annotations gene_1, gene_2, etc as same as gene
                base = gene.split("_")[0]
                genes.append(base)
            else:
                genes.append(gene)
            
    
    genes = set(genes) #don't save duplicate gene entries
    
    return contigs, most_genes, genes, genes_by_contig
    
def readGenes(geneFileName):

    genesFile = open(geneFileName,"r")
    
    lines = genesFile.readlines()
    
    genesFile.close()
    
    lines = [line.rstrip("\n") for line in lines]
    
    return lines
    
def checkDuplicates(genes_by_contig, all_genes):
    #returns True if a gene appears at least twice across all contigs
    duplicates_flag = False
    
    for gene in all_genes:
        # print(gene)
        acc = 0
        
        for gene_set in genes_by_contig:
            for annot in gene_set:
                if "_" in annot: #treats multi annotations gene_1, gene_2, etc as same as gene
                    base = annot.split("_")[0]
                    if base == gene:
                        acc += 1
                else:
                    if annot == gene:
                        acc +=1
        # print(acc)
        if acc > 1:
            duplicates_flag = True
    # print(duplicates_flag)
    return duplicates_flag
    
def checkWithinContigDuplicates(genes_by_contig, all_genes):
    #returns True if a gene appears at least twice in any single contig
    duplicates_flag = False
    for gene_set in genes_by_contig:
        for gene in all_genes:
            acc = 0
            for annot in gene_set:
                if "_" in annot: #treats multi annotations all as one e.g.  cox1_1, cox1_2, etc as same as cox1
                    # print("CHECK")
                    base = annot.split("_")[0]
                    if base == gene:
                        acc += 1
                        # print("CHECK2")
                else:
                    if annot == gene:
                        acc +=1
            # print(acc)
            if acc > 1:
                duplicates_flag = True
    # print(duplicates_flag)
    return duplicates_flag
    
def writeOutput(contigs, most_genes, genes, species, all_genes, dups_detected, within_contig_dups):

    #outString columns defined as follows
    #Assembly_Name	Number_Contigs	Number_Genes	Number_genes_in_best_contig Duplicates  Within_Contig_Duplicates    individual_gene_content (1 column per gene)
    summary_header="Species\tNumber_Contigs\tNumber_Genes\tNumber_genes_in_best_contig\tDuplicates\tDuplicates_within_a_Contig\tindividual_gene_content\n"
    
    outFileName = species + ".one_line_summary.tab"
    
    outFile = open(outFileName,"w")
    
    outFile.write(summary_header)
    
    outString = species + "\t"
    
    outString = outString + str(len(contigs)) + "\t" + str(len(genes)) + "\t" + str(most_genes) + "\t"
    
    outString = outString + str(dups_detected) + "\t" + str(within_contig_dups) + "\t"
    
    for g in all_genes:
    
        if g in genes:
        
            outString = outString + g + "\t"
            
        else:
        
            outString = outString + " \t"
            
    outString = outString.rstrip("\t") + "\n"
    
    outFile.write(outString)
    
    outFile.close()
    
def main():

    summaryFileName, geneFileName ,species = processInputs()
    
    summary_lines = readSummaryFile(summaryFileName)
    
    contigs, most_genes, genes , genes_by_contig = processSummaryFile(summary_lines)
    
    all_genes = readGenes(geneFileName)
    
    dups_detected = checkDuplicates(genes_by_contig, all_genes)
    
    within_contig_dups = checkWithinContigDuplicates(genes_by_contig, all_genes)
    
    writeOutput(contigs, most_genes, genes, species, all_genes, dups_detected, within_contig_dups)
    
main()
