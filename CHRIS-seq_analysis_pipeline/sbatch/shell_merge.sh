#!/bin/sh

mkdir -p 1_merge

for fullpath in ./0_barcode*/*/*_2.txt.gz
do
sleep 0.1

echo $fullpath
sample_dir="${fullpath#*/0_barcode*/}" #gets the file and enclosing director
sample_dir="${sample_dir%%/[^/]*}" #remove the filename to get just directory
bar_directory="${fullpath%/*.*}/"

filename="${fullpath##*/}"    # Strip longest match of */ from start
base="${filename%%.[^.]*}"    #Strip everything after the first period
sample="${base%%_2*}"

merge_out=_merge.out
merge_err=_merge.err



read="${bar_directory#*/}"
read="${read%%/[^/]*}"
read="${read##*_}"
#echo $read


#Detect which read the barcode is on, and merge accordingly to orient the read as sense
if [ $read == "read1" ]
then
in1=_1.txt.gz
in2=_2.txt.gz
elif [ $read == "read2" ]
then
in1=_2.txt.gz
in2=_1.txt.gz
else
in1=_2.txt.gz
in2=_1.txt.gz
fi


echo "#!/bin/bash
#SBATCH --job-name=combine_reads
#SBATCH -o ./1_merge/$sample_dir$base$merge_out
#SBATCH —e ./1_merge/$sample_dir$base$merge_err
#SBATCH --partition=broadwl
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=8
#SBATCH --mem-per-cpu=2000

module load midway2; module load java/11.0.1

sleep 1
#filename="${1##*/}"
#base="${filename%%.[^.]*}"
#sample="${base%%_2*}"
#directory=${1%/*}
#index="${directory##*/}"

./tools/bbmap/bbmerge.sh -in1=$bar_directory$sample$in1 -in2=$bar_directory$sample$in2 -out=./1_merge/$sample_dir$sample.fastq

echo $fullpath
echo $filename
echo $base
echo $sample">./sbatch/jobfile.sbatch


sbatch ./sbatch/jobfile.sbatch $fullpath
done
