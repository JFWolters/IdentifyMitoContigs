#!/bin/bash
hostname

echo "Checking for presence of results directory and deleting if present"
if [ -d results ] ; then
    rm -rf results
fi
if [ ! -d results ]; then
    mkdir results
fi

echo "Designating header of summary file and overwriting it with header only if present"
summary_header="Species\tNumber_Contigs\tNumber_Genes\tNumber_genes_in_best_contig\tDuplicates\tDuplicates_within_a_Contig\tindividual_gene_content"

echo -e $summary_header > all_species_summary.tab

echo "Initializing Complete"
