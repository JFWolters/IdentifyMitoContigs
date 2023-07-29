#!/bin/bash
species=$1
baseDir=$2

source $baseDir/vars.config

$conda init bash
source ~/.bashrc
unset PYTHONPATH
conda activate $python_env


python $scripts_dir/python_scripts/filterSmallContigs.1.py $species.fasta $contig_size_cutoff

conda deactivate
