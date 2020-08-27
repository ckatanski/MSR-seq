Install bbmap in this folder:
https://jgi.doe.gov/data-and-tools/bbtools/bb-tools-user-guide/installation-guide/

Install samtools-1.10 in this folder:
http://www.htslib.org/

Install IGV_2.8.0 in this folder
https://software.broadinstitute.org/software/igv/igvtools_commandline

Install je suite 1.2 in this folder
https://gbcs.embl.de/portal/tiki-index.php?page=Je

Install bowtie2 in this folder
http://bowtie-bio.sourceforge.net/bowtie2/index.shtml





basewise_add_names.py	6/12/2020	Only necessary for human genes. Takes a tsv output format and adds gene names to the "Gene" field.
Clean_up_reads_low_mem.py	6/12/2020	After reads are converted to fasta, this script processes them further: 1) collpase identical reads using UMI; 2) remove UMI sequence; 3) remove barcode sequence; 4)take reverse complement if necessary
sam_to_tsv_tRF.py	6/12/2020	Functions similar to IGV to count mutations at every position, but allos reads to be binned by 3' end. Binning allows focus on fragments. Known bugs. Beware
wig_to_tsv_low_mem.py	6/12/2020	Takes the ".wig" output from IGV and converts it to a nice easy tsv format.
sam_counter.py		8/26/2020	Take the ".sam" output form bowtie2 and counts how many reads map to each reference sequence.
