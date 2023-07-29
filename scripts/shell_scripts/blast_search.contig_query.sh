#!/bin/bash
hostname
#run in species directory

#This script carries out the blast search of mt features as queries and the assembly as subject

base_dir=$1

species=$2 #arbitrary species identifier
echo "Conducting Mt Genome Blast Searches for $species"

scripts_dir=$3 #directory containing python scripts

source $base_dir/vars.config

#the following variables should be set in vars.config
# evalue=1
# word_size=16
# dust="no"
outfmt=5 #cannot be changed

assembly=../$species.fasta

#mito_sources is set as the full path in vars.config

echo "Initiating Contig Query Search"
#blast parameters are set in vars.config
#common ones to change are included (evalue, word_size, dust)
#remainder are left at default and this script would need to modified to change them
$blastn -query $assembly -subject $mito_sources -outfmt '6 qseqid sseqid qcovs pident evalue score qstart qend sstart send' -out $species.contig_query.tab -evalue $evalue -word_size $word_size -dust $dust

cov_cutoff=25 #percent out of 100

$conda init bash
source ~/.bashrc
unset PYTHONPATH
conda activate $python_env

echo "Filtering and converting blast output"
python $scripts_dir/python_scripts/find_mito_contigs.5.py $species.contig_query.tab $cov_cutoff
echo "Contig Query Search Complete"

echo "Summarizing Blast results for contig query search"
python $scripts_dir/python_scripts/summarizeMtBlast.2.2.py $assembly $species.contig_query.cov_filtered.tab
echo "summarizing complete"

conda deactivate
