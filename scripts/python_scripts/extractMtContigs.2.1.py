##Adapted from extractBestMFANNOTContig.2.py
##Returns all identified Mt contigs

##V2.1 updates

##removed making directory mt_contigs since this is handled now in make_directory_structure
##added modifications from V3 (chtc specific version for easier handling), which includes removal of fail file and creation of generic summary file
##all list files are now assumed to contain full path to each file


##V2 update
##Modified to work with V2 of MFANNOT pipeline that records annotations in gff3 format.
##also extracts the genbank formats into one file as well.
import sys
import os
import shutil

def processInputs():

    summaryFileName = sys.argv[1]
    
    genes_cutoff = int(sys.argv[2])
    
    path_to_contigs = sys.argv[3]
    
    path_to_annotations = sys.argv[4]
    
    species = sys.argv[5]
    
    return summaryFileName , genes_cutoff , path_to_contigs, path_to_annotations , species
    
def readSummaryFile(summaryFileName):

    summaryFile = open(summaryFileName,"r")
    
    lines = summaryFile.readlines()
    
    summaryFile.close()
    
    return lines
    
    
def processSummaryFile(lines, genes_cutoff):
    header = lines.pop(0) #remove header line

    lines = [line.rstrip("\n") for line in lines]
    
    lines = [line.split("\t") for line in lines]
    
    
    # lines = [line for line in lines if len(line) > 3] #remove entries with no gene hits
    
    lines = [line for line in lines if len(line) > 1] #remove empty lines
    # for line in lines:
        # print(line)
    lines = [line for line in lines if int(line[2]) >= genes_cutoff]
    base_contig_names = [line[0] for line in lines]
    
    out_lines = [header]
    out_lines.extend(lines)
    # print(out_lines)
    # print(type(out_lines))
    return base_contig_names, out_lines
    
    
def writeOutput(contigs, genes_cutoff, path_to_contigs , path_to_annotations, species):

    summaryFile = open(species + ".mt_contigs_summary.txt","w")
    summaryFile.write("%s contigs with at least %s genes found\n" % (len(contigs), genes_cutoff))
    summaryFile.close()
        
    
    if len(contigs) >= 1:
        fasta = [contig_name + ".fasta" for contig_name in contigs]
        gffs = [ contig_name + ".gff" for contig_name in contigs]
        gb = [contig_name + ".gb" for contig_name in contigs]
        
        contig_paths = [path_to_contigs + contig for contig in fasta]
        gff_paths = [path_to_annotations + gff for gff in gffs]
        gb_paths = [path_to_annotations + gb_file_name for gb_file_name in gb]
        
        outContigsFileName =     species+".mt_contigs.fasta"
        outGFFFileName = species + ".mt_contigs.gff"
        outGBFileName = species + ".mt_contigs.gb"
        
        outContigsFile = open(outContigsFileName,"w")
        outGFFFile = open(outGFFFileName, "w")
        outGBFile = open(outGBFileName, "w")
        #prepare header for gff
        outGFFFile.write("##gff-version 3\n")
        
        for i in range(len(contig_paths)):
            contig_path = contig_paths[i]
            gff_path = gff_paths[i]
            gb_path = gb_paths[i]
            if os.path.exists(contig_path):
                inContigFile = open(contig_path,"r")
                lines=inContigFile.readlines()
                inContigFile.close()
                for line in lines:
                    outContigsFile.write(line)
            else:
                print("ERROR CONTIG NOT FOUND IN",path_to_contigs)
            if os.path.exists(gff_path):
                inGFFFile = open(gff_path,"r")
                lines = inGFFFile.readlines()
                inGFFFile.close()
                lines.pop(0) #remove gff3 version header line
                for line in lines:
                    if line.startswith("##"): #perhaps this section should be specific to sequence-region header lines? Leaving generic for now to catch different types of header info
                        outGFFFile.write(line)
            else:
                print("Error", gff_path, "Not Found")
            if os.path.exists(gb_path):
                inGBFile = open(gb_path,"r")
                lines=inGBFile.readlines()
                inGBFile.close()
                for line in lines:
                    outGBFile.write(line)
            else:
                print("ERROR genbank file", gb_path, "not found")
        for i in range(len(contig_paths)):
            gff_path = gff_paths[i]
            if os.path.exists(gff_path):
                inGFFFile = open(gff_path,"r")
                lines = inGFFFile.readlines()
                inGFFFile.close()
                for line in lines:
                    if not line.startswith("##"):
                        outGFFFile.write(line)
        outContigsFile.close()
        outGFFFile.close()
        outGBFile.close()
        
        
def writeAnnotationSummary(out_lines, species):
    outFileName = species + ".mt_contigs.annotation_summary.tab"
    
    outFile = open(outFileName,"w")
    header = out_lines.pop(0)
    outFile.write(header)
    for line in out_lines:
        out_string = ""
        for item in line:
            out_string = out_string + item + "\t"
        out_string = out_string.rstrip("\t") + "\n"
        outFile.write(out_string)
    outFile.close()

def main():

    summaryFileName , genes_cutoff , path_to_contigs , path_to_annotations , species= processInputs()
    
    # print(species)
    
    summary_lines = readSummaryFile(summaryFileName)
    
    contig_names , out_lines = processSummaryFile(summary_lines, genes_cutoff)
    
    writeOutput(contig_names, genes_cutoff, path_to_contigs , path_to_annotations , species)
    
    writeAnnotationSummary(out_lines, species)
    
main()

