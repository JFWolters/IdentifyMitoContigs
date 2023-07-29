#!/bin/bash
hostname
#run in species directory
species=$1
base_dir=$2
source $base_dir/vars.config
scripts_dir=$3

$conda init bash
source ~/.bashrc
unset PYTHONPATH
conda activate $python_env



#in the case where no contigs met the annotation criteria
#no gffs will exist
#therefore it is necessary to make a blank file in this case
#and the summary will run and recognize there was nothing annotated and thus nothing to summarize

if [ ! -f $species.annotation_file_list.txt ]; then
    touch $species.annotation_file_list.txt
    echo "Creating empty annotation file list (No annotation files exist)"
fi

if [ ! -f $species.gb_file_list.txt ]; then
    touch $species.gb_file_list.txt
    echo "Creating empty gb file list (No annotation files exist)"
fi

if [ ! -f $species.gff_file_list.txt ]; then
    touch $species.gff_file_list.txt
    echo "Creating empty genbank file list (None found)"
fi

if [ -f $species.annotation_summary.tab ]; then
    rm $species.annotation_summary.tab
    echo "Removing pre-existing annotation summary"
fi

echo "Summarizing Annotations"
# echo "$python $scripts_dir/python_scripts/summarizeMFANNOT.7.5.py $gene_targets $species.gb_file_list.txt $species"

python $scripts_dir/python_scripts/summarizeMFANNOT.7.5.py $gene_targets $species.gb_file_list.txt $species
#generates output $species.annotation_summary.tab

conda deactivate
