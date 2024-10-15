import pandas as pd
import os

os.makedirs('/storage_1/KF07453/ncbi-blast-2.16.0+/blast_result_to_plot/')


df = pd.read_csv('/storage_1/KF07453/ncbi-blast-2.16.0+/blast_result_asvtable/asv.csv')
pipe = ['ctrl', 'M', 'SA', 'SAM'] #在此輸入需分析的組別

sci = df.iloc[:10,0].values
pipeline = []
count = 0
for i in range(0, len(pipe)):
    for j in range(0, 11):
        if j < 10:
            pipeline.append(sum(df.iloc[j,i*4+1:i*4+5]))
            count += sum(df.iloc[j,i*4+1:i*4+5])
        else:
            group_sum = 0
            for k in range(1, 5):
                group_sum += sum(df[pipe[i]+"_"+str(k)])
            pipeline.append(group_sum-count)
            count = 0
sci_out = []
for i in range(0, len(pipe)):
    for j in range(0, 11):
        if j < 10:
            sci_out.append(sci[j])
        else:
            sci_out.append("Other")
group = []
for i in range(0, len(pipe)):
    for j in range(0, 11): #這邊可以調整成想要top多少的bacteria abundance
        group.append(pipe[i])
dic = {"group":group,
       "sci_name":sci_out,
       "abundance":pipeline}
df_o = pd.DataFrame(dic)
df_o.to_csv('/storage_1/KF07453/ncbi-blast-2.16.0+/blast_result_to_plot/to_plot.csv', index = False)
