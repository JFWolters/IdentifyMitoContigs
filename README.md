# IdentifyMitoContigs
Identify putative mitochondrial contigs from existing whole genome assemblies

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
