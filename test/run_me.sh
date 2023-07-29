#!/bin/bash

source vars.config

IFS=""

base_dir=$(pwd)

bash $scripts_dir/shell_scripts/initialize.sh

cd results

while read line ; do

    species=$(echo $line | cut -f 1)
    assemblyFileName=$(echo $line | cut -f 2)


    bash $scripts_dir/shell_scripts/make_directory_structure.sh $species $assemblyFileName $scripts_dir


    #Blast Search Feature Query
    cd $species/blast_search

    bash $scripts_dir/shell_scripts/blast_search.feature_query.sh $base_dir $species $scripts_dir


    #Blast Search Contig Query
    bash $scripts_dir/shell_scripts/blast_search.contig_query.sh $base_dir $species $scripts_dir


    #Select Contigs to Annotate
    cd ..

    bash $scripts_dir/shell_scripts/select_contigs_to_annotate.sh $base_dir $species $scripts_dir



    #Split Assembly into Individual Contigs
    cd all_contigs

    bash $scripts_dir/shell_scripts/split_assembly.sh $species $base_dir


    #Run the Annotation on the Selected Contigs
    cd ../annotations

    bash $scripts_dir/shell_scripts/run_annotation.sh $species $base_dir

    #Convert the MFANNOT files into GB and GFF

    bash $scripts_dir/shell_scripts/convert_mfannot2gff.sh $species $base_dir


    #Summarize the Annotations

    cd ..

    bash $scripts_dir/shell_scripts/summarize_annotations.sh $species $base_dir $scripts_dir


    #final summary including density filter

    bash $scripts_dir/shell_scripts/final_summary.sh $species $base_dir


    #Extract the Mitochondrial Contigs and Annotations

    cd mt_contigs

    bash $scripts_dir/shell_scripts/extract_Mt_contigs.sh $species $base_dir $scripts_dir
    
    cd ../..
done < $inFileName
