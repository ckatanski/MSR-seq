#!/bin/sh

reference=./ref_seq/bowtie2_index/Escherichia_tRNA_reference/Escherichia_tRNA_reference
mkdir -p 3_bowtie2

index_file="${reference##*/}"
mkdir -p ./3_bowtie2/$index_file
suffix=.sam

for fullpath in ./2_fasta/*.fasta
do
sleep 0.1
filename="${fullpath##*/}"    # Strip longest match of */ from start
base="${filename%%.[^.]*}"    #Strip everything after the first period

echo "#!/bin/bash
#SBATCH --job-name=bowtie2
#SBATCH --partition=broadwl
#SBATCH -o ./3_bowtie2/$index_file/mapping_stats$base.err
#SBATCH -e ./3_bowtie2/$index_file/mapping_stats$base.err
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=10
#SBATCH --mem-per-cpu=2000

sleep 1
module load midway2

./tools/bowtie2-2.3.3.1-linux-x86_64/bowtie2 -x $reference  -U $fullpath -S ./3_bowtie2/$index_file/$base$suffix -f -p 10 --local

echo -e "$base"
echo -e ""
"> ./sbatch/jobfile.sbatch
sbatch ./sbatch/jobfile.sbatch


done
