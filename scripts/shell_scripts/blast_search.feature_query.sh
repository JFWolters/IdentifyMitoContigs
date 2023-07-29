#!/bin/bash
hostname
#run in species directory

#This script carries out the blast search of mt features as queries and the assembly as subject

base_dir=$1

species=$2 #arbitrary species identifier
echo "Conducting Mt Query Blast Searches for $species"

scripts_dir=$3 #directory containing python scripts

#Set Variables
source $base_dir/vars.config

#the following variables should be set in vars.config
# evalue=1
# word_size=16
# dust="no"
outfmt=5 #cannot be changed


assembly=../$species.fasta


echo "Initiating Mt Feature Query Search"
$blastn -query $mito_features -subject $assembly -outfmt '6 qseqid sseqid qcovs pident evalue score qstart qend sstart send' -out $species.mt_feature_query.tab -evalue $evalue -word_size $word_size -dust $dust
cov_cutoff=70 #percent out of 100

$conda init bash
source ~/.bashrc
unset PYTHONPATH
conda activate $python_env



python $scripts_dir/python_scripts/find_mito_contigs.5.py $species.mt_feature_query.tab $cov_cutoff
echo "Mt Feature Query Search Complete"

#Summarizing blast results
echo "Summarizing Blast results for mt feature query search"
python $scripts_dir/python_scripts/summarizeMtBlast.1.2.py $assembly $species.mt_feature_query.cov_filtered.tab
echo "summarizing complete"

conda deactivate
