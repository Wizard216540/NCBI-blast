# NCBI Blast
先安裝conda環境

官網: https://docs.conda.io/en/latest/miniconda.html
到conda的官方文件(document)中找到你要安裝的miniconda版本(https://docs.anaconda.com/miniconda/miniconda-other-installer-links/)，也有for不同作業系統的，不同miniconda版本還有其預設的python版本，選定一個你要的給他按下去，會得到一個Miniconda3-XXX-XXX.sh，在Linux上安裝的話，只要把這個sh檔上傳到指定目錄下，接著:

`bash Miniconda3-XXX-XXX.sh`

他就會自動安裝。
然後會需要指定miniconda主程式的安裝目錄，預設會在:
`%HOME/miniconda3`

其中%HOME指的就是使用者的家目錄，你可以試試看echo $HOME。當然你也可以指定你要安裝在哪裡。
安裝好之後需要啟動miniconda


啟動方式:
`source /home/KF07453/storage_1/KF07453/miniconda3/bin/activate`

接著你就可以看到
`(base) [KF07453@isb-n7 KF07453]$ `

代表你成功進入miniconda下的初始環境base了~~~


**Create new enviroment`**
以下是建立新的conda環境基本語法:

`conda create --name <env_name> python==3.8`

–name, -n: 指定env的名稱。
python==3.8: 指定env中python的版本

建議一定要指定python版本，不然會安裝到最新的，但很多程式還沒支援到最新的python版本，像是2023的qiime2不支援3.11(當時最新)的python，可以指定裝目前最熱門的python，目前2023.07.28最熱門的是3.8。

安裝好後會得到以下提示:

##### To activate this environment, use
#### #
#####     $ conda activate blast
#### #
##### To deactivate an active environment, use
#### #
#####     $ conda deactivate


接著就依照上面指令activate或deactivate就好囉。

如果有很多conda環境，你可以:

conda env list
就可以看到有哪些conda等著被activate。

如果要切換不同conda環境，建議可以先deactivate當下的，回到base，再去activate你要的環境。



# Blast環境建構
**1. 建立blast分析的Anaconda環境，並啟動該環境:**
```
    conda create -n blast python==3.8
    conda activate blast
```

**2. 下載blast folder**
```
    wget https://ftp.ncbi.nlm.nih.gov/blast/executables/blast+\
    /LATEST/ncbi-blast-2.16.0+-x64-linux.tar.gz
    
    tar -zxvf ncbi-blast-2.16.0+-x64-linux.tar.gz
```

**3. 添加環境變數到配置文件中**
```
cd ncbi-blast-2.16.0+/bin/
echo 'export PATH=$PATH:/storage_1/KF07453/ncbi-blast-2.16.0+/bin' >> ~/.bashrc
source ~/.bashrc

```

**4. 測試環境是否安裝完成**
`blastp -version`

若有成功安裝，會顯示
```
(base) [KF07453@isb-n5 bin]$ blastp -version
blastp: 2.16.0+
 Package: blast 2.16.0, build Jun 25 2024 08:58:03
```


**5. 本機端資料庫下載**
下載資料庫後即可使用

`wget -c https://ftp.ncbi.nlm.nih.gov/blast/db/FASTA/nt.gz`  
`tar -xzvf 16S_ribosomal_RNA.tar.gz`  
`wget ftp://ftp.ncbi.nlm.nih.gov/blast/db/taxdb.tar.gz`  
`tar -zxvf taxdb.tar.gz`  


# NCBI Blast比對

**1. Seqtk toolkit安裝**
因NCBI Blast只能使用fasta格式，故須用seqtk toolkit將fastq.gz格式轉換為fasta格式

```
git clone https://github.com/lh3/seqtk.git;
cd seqtk; make
echo 'export PATH=$PATH:/storage_1/KF07453/ncbi-blast-2.16.0+/seqtk/' >> ~/.bashrc
source ~/.bashrc
conda activate blast
```
![messageImage_1728954884722](https://hackmd.io/_uploads/rJjGfHjyyx.jpg)



**2. fasta格式轉換**
`seqtk seq -a ./xxx.fastq.gz > ./xxx.fasta`  
修改test.sh中的路徑並執行後，即可輸出.fasta格式  
![messageImage_1728958994412](https://hackmd.io/_uploads/r1nLG8iJ1l.jpg)


**3. 使用NCBI 16S_rRNA 資料庫進行序列之比對**  
修改pigmicrobiota_blast.py中的路徑後執行，與先前下載好的16S_rRNA資料庫進行比對  
一個樣本比對約需50分鐘，建議使用nohup  
最後會輸出比對結果之txt檔案  

`python pigmicrobiota_blast.py`

`blastn -db /storage_1/KF07453/ncbi-blast-2.16.0+/16S_ribosomal_RNA -query {file} -evalue 1e-50 -out {output_file} -outfmt '7 qseqid sscinames sseqid sgi sacc evalue bitscore' -max_target_seqs 5 -num_threads 6`

-db: 比對的資料庫位置  
-query: 要進行比對的fasta檔案  
-evalue: 統計學上的期望值，估計在隨機序列中出現相同或更好的比對的機率(在隨機數據庫搜索中，預期會出現多少個相同得分或更好的序列比對)，e值越低結果越準確  
-out: 輸出的檔案  
-outfmt: 輸出檔案的格式  
-max_target_seqs:最多比對到的序列  
-num_threads: 使用的cpu數量  

![圖片1](https://hackmd.io/_uploads/BkxXkwsJkx.png)


**4. 統計每個樣本中的微生物數量**  
先安裝pandas套件供後續分析  
`pip install pandas`  

修改result_to_table.py中的路徑並執行，統計每個樣本中各序列比對到的微生物數量  

`python result_to_table.py`

![messageImage_1728968010410](https://hackmd.io/_uploads/SyXDSuikJx.jpg)


**5. 將所有樣本之統計結果彙整成單一個檔案**  
修改toAsvtable.py中的路徑並執行，統計每個微生物在各樣本中的數量，並按數量排序(高到低)  
最後統整成一個csv檔案  

`python toAsvtable.py`

![messageImage_1728968397280](https://hackmd.io/_uploads/BkXJPOi11g.jpg)


**6. 選擇top 10 abundance之資料進行繪圖**

修改to_plot.py中的路徑並執行，輸出to_plot.csv  

於本機端使用R ggplot2進行繪圖  
```
data <- read.csv("to_plot.csv", header=T)

library(ggplot2)

ggplot(data, aes(x = sci_name, y = abundance, fill = group)) +
geom_bar(stat = "identity") +
theme(axis.text.x = element_text(angle = 45, hjust = 1)) +  # Rotate x-axis labels
labs(title = "Abundance of Bacterial Species", x = "Species", y = "Abundance")


ggsave('top10_abundance.png')
```
![top10_abundance](https://hackmd.io/_uploads/H1P0kKi11l.png)





