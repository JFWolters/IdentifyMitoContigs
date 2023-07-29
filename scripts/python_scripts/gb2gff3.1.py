#copied from https://github.com/nextgenusfs/genome_scripts/blob/master/gb2gff.py

from Bio import SeqIO
import sys

gene_count=1
tRNA_count=1
ori_count = 1
ncRNA_count=1
rRNA_count=1
sys.stdout.write("##gff-version 3\n")
with open(sys.argv[1], 'rU') as gbk:
    for record in SeqIO.parse(gbk, 'genbank'):
        region_string = "##sequence-region %s %s %s\n" % (record.id, 1 , len(record.seq)) 
        sys.stdout.write(region_string)
gbk.close()

with open(sys.argv[1], 'rU') as gbk:
    for record in SeqIO.parse(gbk, 'genbank'):
        landmark_string = "%s\tGenbank\tregion\t1\t%s\t.\t+\t.\tID=%s;Name=%s\n" % (record.id,len(record.seq),record.id,record.id)
        sys.stdout.write(landmark_string)
        for f in record.features:
            # print(f)
            transcript_count=1 #in current execution this never changes
            mRNA_count = 1
            #if a gene can have multiple transcripts this should increment for each one
            if f.type == 'CDS':
                try:
                    gene_name = f.qualifiers['gene'][0]
                except KeyError:
                    try:
                        gene_name = f.qualifiers['note'][0]
                    except KeyError:
                        gene_name = "Unidentified_gene_check_keys_in_genbank"
                gene_name = gene_name.replace(";","_")
                gene_name = gene_name.replace(",","_")
                gene_uid = "gene-" + str(gene_count) #arbitrary identifier for gene
                chr = record.id #name of chromosome
                product = f.qualifiers['product'][0] #usually common name of protein product
                product = product.replace(";","_")
                product = product.replace(",","_")
                start = f.location.nofuzzy_start + 1
                end = f.location.nofuzzy_end
                strand = f.location.strand
                if strand == 1:
                    strand = '+'
                elif strand == -1:
                    strand = '-'
                num_exons = len(f.location.parts)
                current_phase = 0
                sys.stdout.write("%s\tGenBank\tgene\t%s\t%s\t.\t%s\t.\tID=%s;Name=%s\n" % (chr, start, end, strand, gene_uid,gene_name))
                # transcript_uid = "%s-transcript-%s" % (gene_uid,transcript_count)
                # transcript_name = "%s-transcript-%s" % (gene_name,transcript_count)
                # sys.stdout.write("%s\tGenBank\ttranscript\t%s\t%s\t.\t%s\t.\tID=%s;Parent=%s;Name=%s;product=%s\n" % (chr, start, end, strand, transcript_uid,gene_uid, gene_name,product))
                
                mRNA_uid = "%s-mRNA-%s" % (gene_uid,mRNA_count)
                mRNA_name = "%s-mRNA-%s" % (gene_name,mRNA_count)
                sys.stdout.write("%s\tGenBank\tmRNA\t%s\t%s\t.\t%s\t.\tID=%s;Parent=%s;Name=%s;product=%s\n" % (chr, start, end, strand, mRNA_uid,gene_uid, gene_name,product))                
                
                if num_exons < 2: #only a single exon
                    ex_start = str(f.location.nofuzzy_start + 1)
                    ex_end = str(f.location.nofuzzy_end)
                    # exon_uid = "%s-transcript-%s-exon-1" % (gene_uid,transcript_count)
                    # exon_name = "%s-transcript-%s-exon-1" % (gene_name,transcript_count)
                    # sys.stdout.write("%s\tGenBank\texon\t%s\t%s\t.\t%s\t.\tID=%s;Parent=%s;Name=%s\n" % (chr, ex_start, ex_end, strand, exon_uid, transcript_uid, exon_name))
                    exon_uid = "%s-transcript-%s-exon-1" % (gene_uid,mRNA_count)
                    exon_name = "%s-transcript-%s-exon-1" % (gene_name,mRNA_count)
                    sys.stdout.write("%s\tGenBank\texon\t%s\t%s\t.\t%s\t.\tID=%s;Parent=%s;Name=%s\n" % (chr, ex_start, ex_end, strand, exon_uid, mRNA_uid, exon_name))

                    cds_uid= "%s-mRNA-%s-CDS-1" % (gene_uid,mRNA_count)                    
                    cds_name = "%s-mRNA-%s-CDS-1" % (gene_name,mRNA_count)
                    sys.stdout.write("%s\tGenBank\tCDS\t%s\t%s\t.\t%s\t%i\tID=%s;Parent=%s;Name=%s\n" % (chr, ex_start, ex_end, strand, current_phase, cds_uid,mRNA_uid,cds_name))
                    
                else: #more than 1 exon, so parts sub_features
                    for i in range(0,num_exons):
                        ex_start = str(f.location.parts[i].nofuzzy_start + 1)
                        ex_end = str(f.location.parts[i].nofuzzy_end)
                        ex_num = i + 1
                        exon_uid = "%s-transcript-%s-exon-%s" % (gene_uid,mRNA_count,ex_num)
                        exon_name = "%s-transcript-%s-exon-%s" % (gene_name,mRNA_count,ex_num)
                        sys.stdout.write("%s\tGenBank\texon\t%s\t%s\t.\t%s\t.\tID=%s;Parent=%s;Name=%s\n" % (chr, ex_start, ex_end, strand, exon_uid,mRNA_uid,exon_name))
                        cds_uid = "%s-transcript-%s-CDS-%s" % (gene_uid,mRNA_count,ex_num)
                        cds_name = "%s-transcript-%s-CDS-%s" % (gene_name,mRNA_count,ex_num)
                        sys.stdout.write("%s\tGenBank\tCDS\t%s\t%s\t.\t%s\t%i\tID=%s;Parent=%s;Name=%s\n" % (chr, ex_start, ex_end, strand, current_phase, cds_uid, mRNA_uid,cds_name))
                        current_phase = (current_phase - (int(ex_end) - int(ex_start) + 1)) % 3
                        if current_phase == 3:
                            current_phase = 0
                ###Handle any intron entries that may correspond to this CDS
                #this may screw up if one "gene" corresponds to multiple "cds" in the genbank file
                introns = []
                intron_count = 1
                for f in record.features:
                    if f.type == "intron":
                        if f.qualifiers["gene"][0] == gene_name:
                            intron_uid = "%s-intron-%s" % (mRNA_uid,intron_count)
                            intron_name = "%s-mRNA-%s-intron-%s" % (gene_name,mRNA_count, intron_count)
                            sys.stdout.write("%s\tGenBank\tintron\t%s\t%s\t.\t%s\t%i\tID=%s;Parent=%s;Name=%s\n" % (chr, ex_start, ex_end, strand, current_phase, intron_uid, mRNA_uid,intron_name))
                            intron_count = intron_count + 1
                            
                
                
                gene_count = gene_count + 1 #increment the gene_count so each one is unique
                mRNA_count = mRNA_count + 1
                transcript_count = transcript_count + 1 #increment the transcript_count so all transcript for a gene are unique
                #note that mfannot annotation does not recognize transcripts shared by a gene
                #so every gene only has 1 transcript, and thus this incrementing doesn't matter
                
            if f.type == 'tRNA': #currently can't handle spliced tRNAs
                tRNA_uidasgene = "gene-" + str(gene_count)
                tRNA_uidastRNA = "%s-tRNA-%s" % (tRNA_uidasgene,tRNA_count)
                start = str(f.location.nofuzzy_start + 1)
                end = str(f.location.nofuzzy_end)
                strand = f.location.strand
                if strand == 1:
                    strand = '+'
                elif strand == -1:
                    strand = '-'
                product = f.qualifiers['product'][0]
                product = product.replace(";","_")
                product = product.replace(",","_")
                chr = record.id
                sys.stdout.write("%s\tGenBank\tgene\t%s\t%s\t.\t%s\t.\tID=%s\n" % (chr, start, end, strand, tRNA_uidasgene))
                sys.stdout.write("%s\tGenBank\ttRNA\t%s\t%s\t.\t%s\t.\tID=%s;Parent=%s;product=%s\n" % (chr, start, end, strand, tRNA_uidastRNA, tRNA_uidasgene, product))
                # exon_uid = "%s-exon-1" % (tRNA_uidastRNA)
                # sys.stdout.write("%s\tGenBank\texon\t%s\t%s\t.\t%s\t.\tID=%s;Parent=%s\n" % (chr, start, end, strand, exon_uid, tRNA_uidastRNA))
                tRNA_count = tRNA_count + 1
                gene_count = gene_count + 1 #increment the gene_count so each one is unique
            if f.type == 'gene':
                gene_uid = "gene-%s" % (gene_count)
                try:
                    gene_name = f.qualifiers['gene'][0]
                except KeyError:
                    try:
                        gene_name = f.qualifiers['locus_tag'][0]
                    except KeyError:
                        gene_name = "Unidentified_gene_check_keys_in_genbank"
                start = str(f.location.nofuzzy_start + 1)
                end = str(f.location.nofuzzy_end)
                strand = f.location.strand
                if strand == 1:
                    strand = '+'
                elif strand == -1:
                    strand = '-'
                chr = record.id
                sys.stdout.write("%s\tGenBank\tgene\t%s\t%s\t.\t%s\t.\tID=%s;Name=%s\n" % (chr, start, end, strand, gene_uid,gene_name))
                gene_count = gene_count + 1
                
            if f.type == "rep_origin":
                ori_uid = "origin_of_replication-%s" % (ori_count)
                ori_note = f.qualifiers['note'][0]
                ori_note = ori_note.replace(";","_")
                ori_note = ori_note.replace(",","_")
                start = str(f.location.nofuzzy_start + 1)
                end = str(f.location.nofuzzy_end)
                strand = f.location.strand
                if strand == 1:
                    strand = '+'
                elif strand == -1:
                    strand = '-'
                chr = record.id
                sys.stdout.write("%s\tGenBank\torigin_of_replication\t%s\t%s\t.\t%s\t.\tID=%s;Name=%s\n" % (chr, start, end, strand, ori_uid,ori_note))
                ori_count = ori_count + 1
                
            if f.type == "ncRNA":
                gene_uid = "gene-%s" % (gene_count)
                try:
                    gene_name = f.qualifiers['gene'][0]
                except KeyError:
                    gene_name = f.qualifiers['product'][0]
                gene_name = gene_name.replace(";","_")
                gene_name = gene_name.replace(",","_")
                

                ncRNA_uid = "ncRNA_gene-%s" % (ncRNA_count)
                ncRNA_name = gene_name
                start = str(f.location.nofuzzy_start + 1)
                end = str(f.location.nofuzzy_end)
                strand = f.location.strand
                if strand == 1:
                    strand = '+'
                elif strand == -1:
                    strand = '-'
                chr = record.id
                sys.stdout.write("%s\tGenBank\tgene\t%s\t%s\t.\t%s\t.\tID=%s;Name=%s\n" % (chr, start, end, strand, gene_uid,gene_name))
                sys.stdout.write("%s\tGenBank\tncRNA_gene\t%s\t%s\t.\t%s\t.\tID=%s;Name=%s\n" % (chr, start, end, strand, ncRNA_uid,ncRNA_name))
                ncRNA_count = ncRNA_count + 1
                gene_count = gene_count + 1
            if f.type == 'rRNA':
                gene_name = f.qualifiers['gene'][0]
                gene_uid = "gene-" + str(gene_count) #arbitrary identifier for gene
                chr = record.id #name of chromosome
                product = f.qualifiers['product'][0] #usually common name of rRNA
                product = product.replace(";","_")
                product = product.replace(",","_")
                start = f.location.nofuzzy_start + 1
                end = f.location.nofuzzy_end
                strand = f.location.strand
                if strand == 1:
                    strand = '+'
                elif strand == -1:
                    strand = '-'
                num_exons = len(f.location.parts)
                current_phase = 0
                sys.stdout.write("%s\tGenBank\tgene\t%s\t%s\t.\t%s\t.\tID=%s;Name=%s\n" % (chr, start, end, strand, gene_uid,gene_name))
                rRNA_uid = "%s-rRNA-%s" % (gene_uid,rRNA_count)
                rRNA_name = "%s-rRNA-%s" % (gene_name,rRNA_count)
                # mrRNA_uid = "%s-transcript-%s" % (gene_uid,transcript_count)
                # transcript_name = "%s-transcript-%s" % (gene_name,transcript_count)
                sys.stdout.write("%s\tGenBank\trRNA\t%s\t%s\t.\t%s\t.\tID=%s;Parent=%s;Name=%s;product=%s\n" % (chr, start, end, strand, rRNA_uid,gene_uid, rRNA_name,product))
                # sys.stdout.write("%s\tGenBank\ttranscript\t%s\t%s\t.\t%s\t.\tID=%s;Parent=%s;Name=%s;product=%s\n" % (chr, start, end, strand, transcript_uid,gene_uid, transcript_name,product))
                if num_exons < 2: #only a single exon
                    ex_start = str(f.location.nofuzzy_start + 1)
                    ex_end = str(f.location.nofuzzy_end)
                    exon_uid = "%s-rRNA-%s-exon-1" % (gene_uid,rRNA_count)
                    exon_name = "%s-rRNA-%s-exon-1" % (gene_name,rRNA_count)
                    sys.stdout.write("%s\tGenBank\texon\t%s\t%s\t.\t%s\t.\tID=%s;Parent=%s;Name=%s\n" % (chr, ex_start, ex_end, strand, exon_uid, rRNA_uid, exon_name))
                else: #more than 1 exon, so parts sub_features
                    for i in range(0,num_exons):
                        ex_start = str(f.location.parts[i].nofuzzy_start + 1)
                        ex_end = str(f.location.parts[i].nofuzzy_end)
                        ex_num = i + 1
                        exon_uid = "%s-rRNA-%s-exon-%s" % (gene_uid,rRNA_count,ex_num)
                        exon_name = "%s-rRNA-%s-exon-%s" % (gene_name,rRNA_count,ex_num)
                        sys.stdout.write("%s\tGenBank\texon\t%s\t%s\t.\t%s\t.\tID=%s;Parent=%s;Name=%s\n" % (chr, ex_start, ex_end, strand, exon_uid,rRNA_uid,exon_name))
                ###Handle any intron entries that may correspond to this rRNA
                #this may screw up if one "gene" corresponds to multiple "cds" in the genbank file
                introns = []
                intron_count = 1
                for f in record.features:
                    if f.type == "intron":
                        if f.qualifiers["gene"][0] == gene_name:
                            intron_uid = "%s-intron-%s" % (transcript_uid,intron_count)
                            intron_name = "%s-rRNA-%s-intron-%s" % (gene_name,rRNA_count, intron_count)
                            sys.stdout.write("%s\tGenBank\tintron\t%s\t%s\t.\t%s\t.\tID=%s;Parent=%s;Name=%s\n" % (chr, ex_start, ex_end, strand, intron_uid, rRNA_uid,intron_name))
                            intron_count = intron_count + 1

                
                
                gene_count = gene_count + 1 #increment the gene_count so each one is unique
                rRNA_count = rRNA_count + 1 #increment the transcript_count so all transcript for a gene are unique
                #note that mfannot annotation does not recognize transcripts shared by a gene
                #so every gene only has 1 transcript, and thus this incrementing doesn't matter
gbk.close()