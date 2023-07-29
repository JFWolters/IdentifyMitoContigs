#!/bin/bash
hostname

species=$1
base_dir=$2
source $base_dir/vars.config
#Run in annotations directory


#Begin annotation

echo "Annotating selected contigs with MFANNOT"

echo "Checking for annotation file list and removing it if present"
if [ -f ../$species.annotation_files.txt ] ; then
    rm ../$species.annotation_files.txt
fi

echo "Initiating Annotations"
while read -r sequence; do

    if [ ! -f $sequence.new ]; then
        echo "Annotating $sequence with MFANNOT"
        date
        $mfannot -g $t_table --sqn ../all_contigs/$sequence.fasta
    fi
done < ../$species.contigs_to_annotate.txt

echo "Adding annotation files to list"
for file in *.new ; do
    readlink -e $file >> ../$species.annotation_file_list.txt
done

echo "Annotation Complete"
