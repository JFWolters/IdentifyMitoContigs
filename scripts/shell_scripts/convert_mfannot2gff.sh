#!/bin/bash
hostname
#run in annotations directory

#linux64.asn2gb requires CentOS7 to run
species=$1
base_dir=$2

source $base_dir/vars.config

echo "Checking for gb file list and removing it if present"
if [ -f ../$species.gb_file_list.txt ] ; then
    rm ../$species.gb_file_list.txt
fi
echo "Checking for gff file list and removing it if present"
if [ -f ../$species.gff_file_list.txt ] ; then
    rm ../$species.gff_file_list.txt
fi

echo "Converting MFANNOT files to gff"

$conda init bash
source ~/.bashrc
unset PYTHONPATH
conda activate $python_env


while read -r base ; do

    if [ ! -f $base.gff ]; then
        echo "Converting Annotation for $base to sqn then GFF3"
        ~/packages/ncbi_file_converters/linux64.asn2gb -i $base.fasta.new.sqn -o $base.gb
        python $scripts_dir/python_scripts/fixGenbankLocus.1.py $base.gb ../all_contigs/$base.fasta
        mv $base.locus_fixed.gb $base.gb
        readlink -e $base.gb >> ../$species.gb_file_list.txt
        python $scripts_dir/python_scripts/gb2gff3.1.py $base.gb > $base.gff
        readlink -e $base.gff >> ../$species.gff_file_list.txt
    fi
done < ../$species.contigs_to_annotate.txt

echo "Conversions complete"

conda deactivate
