#Sam to tRNA style stats

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i") #Input data path
parser.add_argument("-o") #output file path

args = parser.parse_args()

in_file = args.i
out_file = args.o 



import pysam
import time
import subprocess
import random
import os
from Bio import SeqIO
import numpy as np


def main_program(in_file, out_file):

	ref_dict = {}
	with pysam.AlignmentFile(in_file, 'r') as samfile:
		i=0
		tic = time.time()

		for read in samfile.fetch():
			#check flag; rules out reverse complement, no match, multiple matches
			if read.flag != 0:
				continue
			#If its a mapped read, add it to the genome
			ref_dict[read.reference_id] = ref_dict.get(read.reference_id, 0) +1
			#ref_list.append(read.reference_id)
		#print(len(ref_list))
		sorted_list = []

		with open(out_file, "w") as output:
			output.write("name\tcount")
			for entry, count in ref_dict.items():
				name = samfile.getrname(entry)#.split(".")[0]
				#sorted_list.append((name, count))
				output.write("\n")
				output.write(name)
				output.write("\t")
				output.write(str(count))
			#print(sorted(sorted_list, key=lambda x: x[1]))




if __name__=="__main__":
	main_program(in_file, out_file)


