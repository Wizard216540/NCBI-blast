

mkdir -p /storage_1/KF07453/ncbi-blast-2.16.0+/Rawdata_conversion

process_files() {
    folder_name=$1  
    output_folder=$2  


    total_files=$(python3 - <<END
import os
import glob


files = glob.glob('/storage_1/KF07453/ncbi-blast-2.16.0+/Rawdata/$folder_name*.gz')

output = []
for file in files:
    base_name = os.path.basename(file)
    base_name = base_name.replace('.fastq.gz', '').replace('.fq.gz', '').replace('.gz', '')
    output.append(f"{file} {base_name}")


print("\n".join(output))
END
    )


    while read -r i j; do

        command="seqtk seq -a \"$i\" > /storage_1/KF07453/ncbi-blast-2.16.0+/Rawdata_conversion/${j}.fasta"
        echo "Running: $command"
        eval "$command"
    done <<< "$total_files"

    mkdir -p /storage_1/KF07453/ncbi-blast-2.16.0+/Rawdata_conversion/$output_folder
    mv /storage_1/KF07453/ncbi-blast-2.16.0+/Rawdata_conversion/*.fasta /storage_1/KF07453/ncbi-blast-2.16.0+/Rawdata_conversion/$output_folder
}

# Input folder name # Output folder name

process_files "Ctrl*" "Ctrl"
process_files "M*" "M"
process_files "SA_*" "SA"
process_files "SAM*" "SAM"