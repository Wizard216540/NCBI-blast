

import os
import glob


group_list = ['Ctrl', 'M', 'SA', 'SAM']
for group in group_list:
    filename_list=glob.glob(f'/storage_1/KF07453/ncbi-blast-2.16.0+/Rawdata_conversion/{group}/*fasta')
    
    
    for file in filename_list:
        output_file = os.path.splitext(file)[0] + ".txt"
        S = f"blastn -db /storage_1/KF07453/ncbi-blast-2.16.0+/16S_ribosomal_RNA -query {file} -evalue 1e-50 -out {output_file} -outfmt '7 qseqid sscinames sseqid sgi sacc evalue bitscore' -max_target_seqs 5 -num_threads 6"
        os.system(S)