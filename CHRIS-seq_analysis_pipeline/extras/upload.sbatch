#!/bin/bash
#SBATCH --job-name=example_sbatch
#SBATCH --output=GEO_upload.out
#SBATCH --error=GEO_upload.err
#SBATCH --partition=broadwl
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=2000

module load midway2; module load lftp/4.8.4

lftp ftp://geoftp:rebUzyi1@ftp-private.ncbi.nlm.nih.gov <<EOF

cd uploads/katanski_2p4BoY6k/GEO_submission_20200505/
put $1

bye

EOF

