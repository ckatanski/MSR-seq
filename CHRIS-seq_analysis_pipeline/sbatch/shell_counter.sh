#!/bin/sh

reference=./ref_seq/Escherichia_tRNA_reference.fasta
rm $reference.fai

index_file="${reference##*/}"
index_file="${index_file%%.[^.]*}"
echo $index_file
mkdir -p 6_sam_counter/$index_file
suffix=_abundance.tsv

for fullpath in ./3_bowtie2/$index_file/*.sam
do
sleep 0.1

filename="${fullpath##*/}"    # Strip longest match of */ from start
base="${filename%%.[^.]*}"    #Strip everything after the first period

echo "#!/bin/bash
#SBATCH --job-name=kallisto
#SBATCH -o ./6_sam_counter/$index_file/kallisto.out
#SBATCH —e ./6_sam_counter/$index_file/kallisto.err
#SBATCH --partition=broadwl
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=2
#SBATCH --mem-per-cpu=2000

module unload python
module load midway2; module load python/3.5.2


python3 ./tools/sam_counter.py -i $fullpath -o ./6_sam_counter/$index_file/$base.tsv

">./sbatch/jobfile.sbatch
sbatch ./sbatch/jobfile.sbatch

done
