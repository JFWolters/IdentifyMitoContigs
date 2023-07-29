#Takes in an annotated genome
#in genbank or embl flat text format
#writes out a file with features in fasta format

#version changes
#V.7 changes
#swapped the logic to include features listed in bad_types instead
#of excluding features in good_types

#swapped naming format so gene names comes before record.id (accession)
#changed _ in sequence header to " " so that record.id ends up in description

#changed pathing of outFileName so that it is output in directory in which script is run

#v.6
#moved bad_types to be read from an input file
#added type to fasta sequence names in output


import sys
import os
from Bio import SeqIO


def processInputs():
    inFileName = sys.argv[1]

    return inFileName
    
def doWork(records):
    out = []
    names = []
    for record in records:
        for feat in record.features:
            append = True
            if feat.type == "CDS":
                seq = feat.extract(record.seq)
                try:
                    name = str(feat.qualifiers['gene'][0])
                except KeyError:
                    sys.exit("Unidentified gene")
                out.append([name, record.id,feat.type,seq])
    return out

def writeOutput(out , inFileName):
    
    outFileName = os.path.splitext(os.path.basename(inFileName))[0] + ".CDS.fasta"
    
    outFile = open(outFileName,'w')
    for record in out:
        outFile.write('>'+record[0]+ ' ' + record[1]+" " + record[2] + '\n')
        outFile.write(str(record[3])+'\n')
    outFile.close()

def main():
    inFileName = processInputs()
    records = SeqIO.parse(inFileName,"genbank")
    out = doWork(records)
    writeOutput(out , inFileName)

main()
