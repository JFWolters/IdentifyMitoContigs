#!/bin/bash
hostname
#run in mt_contigs directory
species=$1
base_dir=$2

source $base_dir/vars.config

scripts_dir=$3

$conda init bash
source ~/.bashrc
unset PYTHONPATH
conda activate $python_env


echo "Extracting Mt Contigs and Annotations"
python $scripts_dir/python_scripts/extractMtContigs.2.1.py ../$species.annotation_summary.density_filtered.$density_cutoff.tab $genes_cutoff "$base_dir/results/$species/all_contigs/" "$base_dir/results/$species/annotations/" $species

echo "Extraction Complete"

conda deactivate
