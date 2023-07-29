#!/bin/bash
hostname
#run in species directory
base_dir=$1
species=$2
scripts_dir=$3

source $base_dir/vars.config

$conda init bash
source ~/.bashrc
unset PYTHONPATH
conda activate $python_env



echo "Selecting contigs to annotate for $species"


#specify input files
feature_blast=./blast_search/$species.mt_feature_query.cov_filtered.results_summary.txt
contig_blast=./blast_search/$species.contig_query.cov_filtered.results_summary.txt

#Begin Selection
echo "Selecting contigs from feature query search"
python $scripts_dir/python_scripts/selectContigsToAnnotate.1.3.py $feature_blast $max_length $min_hits

cp contigs_to_annotate.txt mt_feature_query.contigs_to_annotate.txt
rm contigs_to_annotate.txt
#only require 1 hit when selecting contigs based on contig_query search method
echo "Selecting contigs from contig query search"
#note that this step overwrites contigs_to_annotate.txt
python $scripts_dir/python_scripts/selectContigsToAnnotate.1.3.py $contig_blast $max_length 1
cp contigs_to_annotate.txt contig_query.contigs_to_annotate.txt
rm contigs_to_annotate.txt

echo "Concatenating contig lists"
cat mt_feature_query.contigs_to_annotate.txt contig_query.contigs_to_annotate.txt > contigs_to_annotate.txt

echo "Removing duplicate contig entries"
python $scripts_dir/python_scripts/uniqueContigs.1.py contigs_to_annotate.txt

if [ -f temp_contigs_to_annotate.txt ] ; then
    echo "Removing residual file if present"
    rm contigs_to_annotate.txt
fi

if [ -f contigs_to_annotate.unique.txt ]; then
    echo "Renaming output"
    mv contigs_to_annotate.unique.txt $species.contigs_to_annotate.txt
fi

conda deactivate
