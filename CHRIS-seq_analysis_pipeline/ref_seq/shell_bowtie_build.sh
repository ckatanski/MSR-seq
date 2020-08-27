#!/bin/sh


REFERENCE_GENOME=Mouse_tRNA_reference_T.fasta


INDEX_NAME="${REFERENCE_GENOME%%.[^.]*}"
mkdir -p bowtie2_index/$INDEX_NAME
echo ./bowtie2_index/$INDEX_NAME/$INDEX_NAME

sbatch ./bowtie2_build.sbatch $REFERENCE_GENOME ./bowtie2_index/$INDEX_NAME/$INDEX_NAME


