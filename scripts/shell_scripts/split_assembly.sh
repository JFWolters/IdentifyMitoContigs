#!/bin/bash

#Run in all_contigs directory

species=$1

base_dir=$2

source $base_dir/vars.config

sequence_file=../$species.fasta

$conda init bash
source ~/.bashrc
unset PYTHONPATH
conda activate $python_env



echo "Splitting assembly into individual contigs"

python $scripts_dir/python_scripts/splitFASTA.1.py $sequence_file

conda deactivate
