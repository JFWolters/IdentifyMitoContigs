#!/bin/bash

###THIS SCRIPT IS DEFUNCT AND NO LONGER USED IN THE PIPELINE
###ALL ANNOTATION QC MUST BE DONE POSTHOC

species=$1
base_dir=$2

annotSummaryFileName=../$species.annotation_summary.tab

source $base_dir/vars.config

header="Contig\tContig_Length\tNum_Genes_Found\tGenes_Found"

tail -n +2 $annotSummaryFileName | cut -f 1 > contig_names.txt

echo -e "$header" > $species.annotation_summary.annot_size_filtered.tab

# exit

while read contig ; do
    #the tab is necessary for the grep so that e.g. s1 doesn't match s10
    summary_line=$(grep -P "$contig""\t" $annotSummaryFileName)
    echo "$summary_line"
    gb_file_name=../annotations/$contig.gb

    python $scripts_dir/python_scripts/genbank2CDS.py $gb_file_name
    # exit
    python $scripts_dir/python_scripts/get_gene_names.py "$summary_line" $contig
    # exit
    touch $contig.flagged_genes.txt
    
    # cat $contig.gene_names.txt
    while read gene_name ; do
        # echo $gene_name
        # cat $cds_dir/$gene_name/$gene_name.size_summary.tab
        mean_size=$(sed '2q;d' $cds_dir/$gene_name/$gene_name.size_summary.tab | cut -f 2 )
        # echo "mean_size" $mean_size
        sd_size=$(sed '3q;d' $cds_dir/$gene_name/$gene_name.size_summary.tab | cut -f 2 )
        # echo "sd_size" $sd_size
        # exit
        python $scripts_dir/python_scripts/extract_gene.py $contig.CDS.fasta $gene_name
        # exit
        python $scripts_dir/python_scripts/calc_contig_sizes.py $contig.CDS.$gene_name.fasta $contig.CDS.$gene_name
        # exit
        check=$($python $scripts_dir/python_scripts/check_size.py $contig.CDS.$gene_name.sizes.tab $mean_size $sd_size)
        # echo $check
        # exit
        if [ $check == "TRUE" ] ; then
            echo $gene_name >> $contig.flagged_genes.txt
        elif [ $check == "FALSE" ] ; then
            echo "$gene_name not flagged for $contig"
        else
            echo "ERROR"
            exit
        fi
        # exit
    done < $contig.gene_names.txt
    
    new_summary_line=$($python $scripts_dir/python_scripts/new_summary_line.py "$summary_line" $contig.flagged_genes.txt)
    
    echo "$new_summary_line" >> $species.annotation_summary.annot_size_filtered.tab
    # exit
done < contig_names.txt

##cleanup

find . -type f -name '*.fasta' -delete
find . -type f -name '*CDS*' -delete
find . -type f -name '*.gene_names.txt' -delete
find . -type f -name '*.flagged_genes.txt' -delete
find . -type f -name contig_names.txt -delete
# find . -type f -name '*sizes*' -delete
# find . -type f -name '*.size_summary.tab' -delete

cp $species.annotation_summary.annot_size_filtered.tab ..
