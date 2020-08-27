#!/bin/sh


for fullpath in ./GEO_submission_20200505/*
do

    sbatch upload.sbatch $fullpath
    echo $fullpath

done
