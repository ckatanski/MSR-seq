#!/bin/bash
#SBATCH --job-name=bowtie2-index
#SBATCH -o ./bowtie2_index/bowtie2_build.out
#SBATCH -e ./bowtie2_index/bowtie2_build.err
#SBATCH --partition=broadwl
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=10
#SBATCH --mem-per-cpu=2000

../tools/bowtie2-2.3.3.1-linux-x86_64/bowtie2-build --threads 10 -f "$1" "$2"

../tools/kallisto/kallisto-0.46.1/src/kallisto index -k 11 -i $2.idx $1
