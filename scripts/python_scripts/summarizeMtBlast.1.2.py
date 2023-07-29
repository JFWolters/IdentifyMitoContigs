###Designed to be run on the output of idenitfy_mito_scaffolds.py

#For each contig, count the number of hits in a blast results file, and the gc % and length of that contig
#Note that if a contig had 0 hits it wont show up in the results file

##V1.2 change notes
#updated to work on output from find_mito_contigs.5.py
#input is tab delimited filtered blast results with mt features as the query
#added os.path tools to better manage output file names



##V1.1 change notes
#input is assumed to be .tab, removed gff related info

import sys
from Bio import SeqIO
from Bio import SeqUtils
import os

class Entry:
    # def __init__(self,contig,feature,start,end,cov,seq,strand):
    def __init__(self,query,sbjct,cov,pident):
        self.query = query
        
        self.sbjct = sbjct
        
        self.cov = float(cov)
        
        self.pident = float(pident)
        
def processInput():
    try:
        inGenomes = sys.argv[1]
        inBlastResults = sys.argv[2] #list of features from the original genome
        

    except IndexError:
        # print('TRIGGERED')
        inGenomes = input('Enter the input Genome:')
        inBlastResults = input('Enter the input Blast Results:')
    return inGenomes,inBlastResults

def readFasta(fasta):
    records = list(SeqIO.parse(fasta,'fasta'))
    return records
    
def readBlastResults(inFileName):
    inFile= open(inFileName,'r')
    blast_results = []
    lines = inFile.readlines()
    lines.pop(0)
    inFile.close()
    for line in lines:
        g = line.rstrip('\n')
        g = g.split('\t')
        #swap the query and sbjct here since the contigs are the subject
        blast_results.append(Entry(g[1],g[0],g[2],g[3]))
    return blast_results
    
def uniqueContigs(blast_results):
    #get unique contigs from list all contig hits
    #eliminate extra info in contig added by blast e.g. gnl|BL_ORD_ID|970639 in
    #gnl|BL_ORD_ID|970639yHMPu5000034867_zygosaccharomyces_bailii_170713.fasNODE_1184_length_2793_cov_150753_ID_73516
    
    contigs = []
    
    for hit in blast_results:
    
        contig = hit.query
        contig = contig.split(" ")[0] #necessary because blast outputs full name but record.id only records first space delimited field
        contigs.append(contig)
        
    return set(contigs)
    
def getGCandLength(contig, records):
    
    matches = []
    
    for record in records:
        if record.id == contig:
            matches.append(record)
    
    if len(matches) == 0:
        return "No Matches", "No Matches"
    elif len(matches) == 1:
        seq_length = len(matches[0].seq)
        gc = SeqUtils.GC(matches[0].seq)
        
        return seq_length, gc
    else:
        return "Multiple Matches", "Multiple Matches"

def countHits(contig, blast_results):
    
    matches = 0
    
    for hit in blast_results:
    
        if contig in hit.query:
        
            matches += 1
    
    return matches
    
def summarizeResults(outFileName, contigs, records, blast_results):
    
    outFile = open(outFileName,"w")
    
    outFile.write("Contig\tHits\tLength\tGC\n")
    
    for contig in contigs:
    
        seq_length, gc = getGCandLength(contig,records)
        
        num_hits = countHits(contig, blast_results)
        
        outString = contig + "\t" + str(num_hits) + "\t" + str(seq_length) + "\t" + str(gc) + "\n"
        
        outFile.write(outString)
        
    print(outFileName, "created")
    
def main():
    inGenomes,inBlastResults = processInput()
    
    records = readFasta(inGenomes)
    
    blast_results = readBlastResults(inBlastResults)
    
    contigs = uniqueContigs(blast_results)
    
    outFileName = os.path.basename(inBlastResults)
    outFileName = os.path.splitext(outFileName)[0] + ".results_summary.txt"
    
    summarizeResults(outFileName, contigs, records, blast_results)

main()


