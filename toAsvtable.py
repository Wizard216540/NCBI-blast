
import pandas as pd
import glob
import os


def ex_col(scilist, df_2):
    sci_1 = scilist
    sci_2 = df_2[df_2.columns[0]]
    count_2 = df_2[df_2.columns[1]]
    same_sci = []
    count_n = list()
    if len(sci_1) > len(sci_2):
        count_n = [0]*len(sci_1)
    else:
        count_n = [0]*len(sci_1)
    for i in range(0, len(sci_1)):
        for j in range(0, len(sci_2)):
            if sci_1[i] == sci_2[j]:
                same_sci.append(j)
                count_n[i] = int(count_2[j])
    df_in = df_2.drop(same_sci)
    
    
    sci_o = pd.concat([sci_1, df_in["sci_names"]], ignore_index=True)
    count_n = pd.Series(data = count_n)
    count_o = pd.concat([count_n, df_in["count"]], ignore_index=True)
    
    return [sci_o, count_o]

# Main
os.makedirs('/storage_1/KF07453/ncbi-blast-2.16.0+/blast_result_asvtable')

path = '/storage_1/KF07453/ncbi-blast-2.16.0+/blast_result_to_table/'

output_path = '/storage_1/KF07453/ncbi-blast-2.16.0+/blast_result_asvtable'



csv_files = glob.glob(path + "*.csv")
pipeline = []
column = []


for file in csv_files:
    file_name = file.split('/')[-1].replace(".csv", "")
    column.append(file_name)


with open(csv_files[0]) as f_1:
    result = []
    df_a = pd.read_csv(f_1)
    sci_name = df_a["sci_names"]
    pipeline.append(df_a["count"])

    for i in range(1, len(csv_files)):
        with open(csv_files[i]) as f_2:
            df_b = pd.read_csv(f_2)
            result = ex_col(sci_name, df_b)
        sci_name = result[0]
        pipeline.append(result[1])


dic = {"sci_name": sci_name}
df = pd.DataFrame(dic)

for i in range(len(column)):
    df[column[i]] = pipeline[i]

df = df.fillna(0)


df["sum"] = df.iloc[:, 1:].sum(axis=1)

# 按照 sum 降序排序
df = df.sort_values(by=["sum"], ascending=False)

# 輸出結果到 CSV 檔案
df.to_csv(f'{output_path}/asv.csv', index=False)


