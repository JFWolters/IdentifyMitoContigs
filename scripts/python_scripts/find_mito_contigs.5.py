##V5 updates
#Significant overhaul
#Now uses blast outfmt 6 tabular output with the following field layout
#qseqid sseqid qcovs pident evalue score qstart qend sstart send

#added os.path functionalities to improve outFileName generation
#changed outFileName to be same as infile but ending with "cov_filtered.tab"


##V4.1 changes
#changed output to ".tab" and removed gff related info

##V4 Changes
#moved blast search to separate script blastSearch.1.py

##V3 change notes
#restructured coverage cutoff
#results are now compared to the sum coverage of all individual hsps in an alignment
#for which the coverage of the hsp was at least 5%
#I removed sequence reporting to accomodate this change

##V2 change notes
#The coverage cutoff is now taken in as a command line input
#to allow this same script to be run flexibly for different searches


##V1.3 change notes
#Changed blast settings to be more conservative (word size from 7 to 16)

import sys

import os


class Entry:
    # def __init__(self,contig,feature,start,end,cov,seq,strand):
    def __init__(self,query,sbjct,cov,pident):
        self.query = query
        
        self.sbjct = sbjct
        
        self.cov = float(cov)
        
        self.pident = float(pident)

def processInputs():
    blastResultsFileName=sys.argv[1]
    cov_filter = float(sys.argv[2]) 
    
    
    return blastResultsFileName, cov_filter
    
def parseBlast(inFileName, cov_filter):

    Entries = []
    
    blast_hits = list(readBlast(inFileName))
    
    num_hits = len(blast_hits)
    
    num_processed = 1
    
    for blast_hit in blast_hits:
    
        
        num_processed = num_processed + 1
        
        if blast_hit.cov > cov_filter :
            Entries.append(blast_hit)
        
    return Entries
    
def readBlast(inFileName):
    blastFile = open(inFileName,'r')
    lines=blastFile.readlines()
    blastFile.close()
    
    lines=[line.rstrip("\n").split("\t") for line in lines]
    
    blast_hits = [ Entry(line[0],line[1],line[2],line[3]) for line in lines]
    
    return blast_hits
    

    
def writeOutput(Entries,inFileName):


    outFileName = os.path.basename(inFileName)
    outFileName = os.path.splitext(outFileName)[0] + ".cov_filtered.tab"
    
    outFile = open(outFileName,'w')
    outFile.write('#Query\tSbjct\tCoverage\tPercent_Identity\n')
    
    
    for entry in Entries:
        outFile.write(entry.query+'\t'+entry.sbjct+'\t'+ \
                      str(entry.cov) + "\t" +str(entry.pident) + '\n')
    outFile.close()
    print(outFileName,'created')
    

    
def main():
    
    blastResultsFileName , cov_filter = processInputs()
    
    Entries = parseBlast(blastResultsFileName, cov_filter)
    
    writeOutput(Entries,blastResultsFileName)

main()
    
