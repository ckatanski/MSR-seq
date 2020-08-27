import argparse
import time
import subprocess
import random
import os
#from Bio import SeqIO
import numpy as np
import time

parser = argparse.ArgumentParser()
parser.add_argument("-i") #Input data path
parser.add_argument("-r") #reference file
parser.add_argument("-o") #output file name

args = parser.parse_args()

in_file = args.i
ref_file = args.r
out_file = args.o


def read_fasta(ref_file):
	#read in reference fasta file
	with open(ref_file) as f:
		genes = f.readlines()

	#make a dictionary keyed by gene name values are catagories etc
	gene_name_dict = {}
	for line in genes:
		if line[0] == ">":
			stuff = line.split()
			#print(stuff)
			gene_name_dict[stuff[0][1:]] = stuff[1:]
	return gene_name_dict

def read_tsv(in_file):
	#read lines
	with open(in_file) as f:
		tidy_pileup = f.readlines()
	return tidy_pileup



def print_tidy(in_file, ref_file, out_file):
	gene_name_dict = read_fasta(ref_file)
	mapped_reads = read_tsv(in_file)
	
	with open(out_file, "w") as o:
		o.write("Gene"+"\t")
		o.write("type"+"\t")
		#o.write("chrom_pos"+"\t")
		#o.write("gene1"+"\t")
		o.write("gene_biotype"+"\t")
		#o.write("transcript_biotype"+"\t")
		o.write("gene_symbol"+"\t")
		o.write(mapped_reads[0])

		for line in mapped_reads[1:]:
			gene_name = line.split("\t")[0]
			gene_info = gene_name_dict[gene_name]

			o.write(gene_name+"\t") #gene name
			o.write(gene_info[0]+"\t") #type
			#o.write(gene_info[1]+"\t") #chromosome
			#o.write(gene_info[2]+"\t") #gene name again
			o.write(gene_info[3][13:]+"\t") #gene_biotype
			#o.write(gene_info[4]+"\t") #transcript biotype
			o.write(gene_info[5][12:]+"\t") #gene_symbol
			#o.write(gene_info[6]+"\t") #description
			o.write(line) #should include a newline character




if __name__ == "__main__":
	print_tidy(in_file, ref_file, out_file)