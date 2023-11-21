# IdentifyMitoContigs
Identify putative mitochondrial contigs from existing whole genome assemblies.

# Input:
A set of whole-genome assemblies that may contain mitochondrial contigs.

# Output:
A fasta of extracted mitochondrial contigs, a summary file for each assembly in "results/[DataID]/mt_contigs", and an overall summary file in "all_species_summary.tab".

# To Run:
1. Copy the scripts and mito_anchors_V4 to directory to hold the pipeline
2. Copy run_me.sh and vars.config into the directory you want to run the pipeline
3. Create a table of input data (tab delimited) in the format: DataID /full/path/to/assembly
4. Edit vars.config to modify settings and provide all necessary file paths.
5. Run run_me.sh as "bash run_me.sh"

# Dependencies :
1. mfannot for mitochondrial genome annotation, see https://github.com/BFL-lab/Mfannot for details
2. BLAST
3. conda (exclusively for running python)
4. python3+ with Biopython in a conda env

# Non-yeast datasets:
The pipeline was designed for use on yeast genomes, but is organism agnostic. Reference genomes for use with yeast are provided in "mito_anchors_V4" and described in "select.strain_info_accessions.tab". If you wish to run it on a different group then change out the files "select_sources.fasta" to include the reference genomes and "select_mito_core_cds.fasta" to include the CDS extracted from those references. Modify the "gene_targets" file as needed to match your desired list of ouput genes (must be in MFANNOT naming format).

# Parallelization on HTCondr:
This pipeline was originally developed for use on HTCondor systems to take advantange of using DAGs for parallelization. The version presented here is not parallelized and is suitable for any UNIX system with bash. If the DAG version of the pipeline would be useful to you please reach out and we would be happy to provide it.

# To Cite:
Reference TBD
