
import pandas as pd
import re
import os
import glob


group_list = ['Ctrl', 'SA', 'M', 'SAM']

os.makedirs('/storage_1/KF07453/ncbi-blast-2.16.0+/blast_result_to_table/', exist_ok=True)

output_path = '/storage_1/KF07453/ncbi-blast-2.16.0+/blast_result_to_table/'


for group in group_list:
    filename_list=glob.glob(f'/storage_1/KF07453/ncbi-blast-2.16.0+/blast_result/{group}/*txt')
    for file in filename_list:

        with open(file, 'r') as fileloop:
            num = 0
            col = "query_id\tsubject_sci_names\tsubject_id\tsubject_gi\tsubject_acc\tevalue\tbit_score\n"
            while True:
                line = fileloop.readline()
                if re.match("#.*", line) != None:
                    num = 0
                else:
                    if num == 0:
                        col += line
                        num += 1
                if not line:
                    break
            col_cut = col.split("\n")
            col_name = ["query_id", "sci_names", "subject_id", "subject_gi", "subject_acc", "evalue", "bit_score"]
            seq_id, sci_name, sub_id, gi, acc, evalue, bit_score = [[], [], [], [], [], [], []]
            for j in range(1, len(col_cut)-1):
                col_cutcut = col_cut[j].split("\t")
                seq_id.append(col_cutcut[0])
                sci_name.append(col_cutcut[1])
                sub_id.append(col_cutcut[2])
                gi.append(col_cutcut[3])
                acc.append(col_cutcut[4])
                evalue.append(col_cutcut[5])
                bit_score.append(col_cutcut[6])
            dict_1 = {"query_id" : seq_id,
                      "subject_sci_names" : sci_name,
                      "subject_id" : sub_id,
                      "subject_gi" : gi,
                      "subject_acc" : acc,
                      "evalue" : evalue,
                      "bit_score" : bit_score}
            df = pd.DataFrame(dict_1)
            
            ans = df['subject_sci_names'].value_counts()
            ans_df = pd.DataFrame({'sci_names':ans.index, 'count':ans.values})
            
            
            output_filename = f"{os.path.basename(file).replace('.txt', '')}.csv"
            ans_df.to_csv(os.path.join(output_path, output_filename), index=False)

