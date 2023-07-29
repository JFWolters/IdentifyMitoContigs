###Runs on the output from summarize_species_results.sh in the identify_mito_scaffolds analysis

###Filters results down to only select contigs for downstream annotation that are small enough and have at least some blast hits

#V1.3 change notes
#removed fasta extension appended to contig names
#now the names in the output should be equal to the contig id

#V1.2 change notes
#Removed writeNewOutput function
#this functionality was moved to the script that runs the annotations

import sys

def processInputs():

    results_summary_file = sys.argv[1]
    
    max_length = int(sys.argv[2])
    
    min_hits = int(sys.argv[3])
    
    results_summary = readSummaryFile(results_summary_file)
    
    return results_summary, max_length, min_hits
    
def readSummaryFile(results_summary_file):

    summaryFile = open(results_summary_file,"r")
    
    lines = summaryFile.readlines()
    
    lines.pop(0) #remove header lines
    
    lines = [line.rstrip("\n") for line in lines]
    
    lines = [line.split("\t") for line in lines]
    
    # print(lines)
    
    return lines
    
def processResults(results, max_length, min_hits):

    output = []
    
    for line in results:
    
        if int(line[2]) < max_length:
        
            if int(line[1]) >= min_hits:
                
                name = line[0]
                
                output.append(name)
                
    return(output)
    
def writeOutput(output):

    outFileName = "contigs_to_annotate.txt"
    
    outFile = open(outFileName,"w")
    
    for item in output:
    
        line = item + "\n"
        
        outFile.write(line)
        
    outFile.close()
    
    print(outFileName, "created")
    

    
def main():

    results_summary, max_length, min_hits = processInputs()
    
    output = processResults( results_summary, max_length, min_hits )
    
    writeOutput(output)
    
main()