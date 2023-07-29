#!/bin/bash
hostname
#run in isr directory

species=$1
assemblyFileName=$2
scripts_dir=$3
echo "Preparing Directory Structure for $species"
echo "Checking for species directory and making it if it isn't present"
if [ ! -d $species ]; then
    mkdir $species
fi

cd $species

echo "Copying assembly into species dir"
if [ ! -f $species.fasta ] ;  then
    cp $assemblyFileName $species.fasta
    python $scripts_dir/python_scripts/fixContigs.1.py $species.fasta
fi

echo "Checking for blast_search directory and making it if it isn't present"
if [ ! -d blast_search ]; then
    mkdir blast_search
fi

echo "Checking for contigs directory and making it if it isn't present"
if [ ! -d all_contigs ]; then
    mkdir all_contigs
fi

echo "Checking for annotations directory and making it if it isn't present"
if [ ! -d annotations ]; then
    mkdir annotations
fi
# echo "Checking for length_check directory and making it if it isn't present"
# if [ ! -d length_check ]; then
    # mkdir length_check
# fi

echo "Checking for final mt_contigs directory and making it if it isn't present"
if [ ! -d mt_contigs ]; then
    mkdir mt_contigs
fi

echo "Preparing directory structure for $species complete"
