#!/bin/bash
species=$1
base_dir=$2

source $base_dir/vars.config

$conda init bash
source ~/.bashrc
unset PYTHONPATH
conda activate $python_env


###Filter based on gene density
echo "Filter Contigs based on gene density"
python $scripts_dir/python_scripts/filter_contigs_by_gene_density.0.2.py $species.annotation_summary.tab $density_cutoff
#generates output $species.annotation_summary.density_filtered.$density_cutoff.tab

###Summarize the annotation summary into one line
python $scripts_dir/python_scripts/summarize_MFANNOT_summary.3.3.py $species.annotation_summary.density_filtered.$density_cutoff.tab $gene_targets $species

tail -n 1 $species.one_line_summary.tab >> $all_summary_file

conda deactivate
