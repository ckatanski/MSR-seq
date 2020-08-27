#!/bin/sh

mkdir -p 2_fasta

for fullpath in ./1_merge/*.fastq
do
sleep 0.1

#Get the name of this file
filename="${fullpath##*/}"    # Strip longest match of */ from start
base="${filename%%.[^.]*}"    #Strip everything after the first period

out=.out
err=.err

suffix=_temp.fasta
suffix2=.fasta

echo "#!/bin/bash
#SBATCH --job-name=BigfastaConvert
#SBATCH -o ./2_fasta/fasta_$base$out
#SBATCH —e ./2_fasta/fasta_$base$err
#SBATCH --partition=broadwl
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=16000

sleep 1
module load midway2;
module load java/11.0.1
module unload python
module load python/3.5.2

./tools/bbmap/reformat.sh -in=$fullpath -out=./2_fasta/$base$suffix
python3 ./tools/Clean_up_reads_low_mem.py -i ./2_fasta/$base$suffix  -o ./2_fasta/$base$suffix2 -c True -rc True
echo -e "$base"

rm ./2_fasta/$base$suffix

"> ./sbatch/jobfile.sbatch
sbatch ./sbatch/jobfile.sbatch

done
