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

def enhance_wig(data_path, ref_path, out_file):
	'''
	stuff
	'''
	#read in reference fasta
	ref_dict = read_reference_fasta(ref_path)
	wig_data = read_wig_file(data_path, ref_dict, out_file)


def read_reference_fasta(ref_path):
	#read in reference fasta
	with open(ref_path) as f:
		lines = f.readlines()
	ref_dict={}
	name=""
	for line in lines:
		if line[0] ==">":
			name = line.split()[0]
			name = name.strip(">")
			seq=""

		elif line == "\n":
			pass #prevents empty lines at the end of file from overwirting sequences

		else:
			seq += line.strip()
			ref_dict[name] = seq #update the dictionary
	return ref_dict

def read_wig_file(data_path, ref_dict, out_file):
	with open(data_path) as f:
		line = f.readline() #Skip the first line
		line = f.readline() #Skip the header
		gene_lines = [] #a list of lines for a single gene

#		oop through the wig file data
		while line:
			#Advance the line reader by 1.
			line = f.readline().strip().split()

			#If this is an empty line don't do anything
			if line == []:
				continue

			#if we're starting a new gene, reset stuff
			if line[0]=="variableStep":
				print_one_gene(gene_lines, out_file, ref_dict)
				gene_lines = []
				gene_lines.append(line)

			#print lines as they come. Yee-haw
			else:
				gene_lines.append(line)
		#Finish off the loop
		print_one_gene(gene_lines, out_file, ref_dict)



def print_one_gene(gene_lines, out_file, ref_dict):

	if gene_lines == []:
		#write a tidy data output
		with open(out_file, "w") as f:
			f.write("gene"+"\t")
			f.write("position"+"\t")
			f.write("base"+"\t")
			f.write("pileup"+"\t")
			f.write("mutation"+"\t")
			f.write("stop"+"\t")
			f.write("A"+"\t")
			f.write("C"+"\t")
			f.write("G"+"\t")
			f.write("T"+"\t")
			f.write("N"+"\t")
			f.write("deletion"+"\t")
			f.write("insertion")

	else: #append actual data
		print()
		print(gene_lines[0][1].split("=")[1])
		print()
		with open(out_file, "a") as file:
			#Set the name and sequence
			name=gene_lines[0][1].split("=")[1]
			seq = ref_dict[name]

			position=[]
			base=[]
			count_A = []
			count_C = []
			count_G = []
			count_T = []
			count_N = []
			count_del=[]
			count_ins=[]

			#read in all the lines
			for line in gene_lines[1:]:
				position.append(int(float(line[0])))
				base.append(seq[int(float(line[0]))-1])
				count_A.append(int(float(line[1]) ))
				count_C.append(int(float(line[2])))
				count_G.append(int(float(line[3])))
				count_T.append(int(float(line[4])))
				count_N.append(int(float(line[5])))
				count_del.append(int(float(line[6])))
				count_ins.append(int(float(line[7])))

			#compute pileup at each position with fancy list comprehension
			pileup = [np.sum((i,j,k,l,m,n,o)) for i,j,k,l,m,n,o in zip(count_A, count_C, count_G, count_T, count_N, count_del, count_ins)]

			#compute mutation rate
			mut_dict = {"A":count_A,"C":count_C,
						"G":count_G,"T":count_T}
			#I got list comprehension inside of list comprehension
			mutation = [sum(mut_dict[B][j] if B!=base else 0 for B in mut_dict.keys()) for j, base in enumerate(base)]
			mutation_rate = []
			for i, j in zip(mutation, pileup):
				if j>0:
					mutation_rate.append(round(i/j, 4))
				else:
					mutation_rate.append(0)
			#mutation_rate = [round(m / p, 4) for m,p in zip(mutation, pileup)]

			#Stop rate calculation (requires lots of n-1 stuff). I used numpy array roll technique to help
			#This was very clever, but I still have divide by zero errors that need tending
			temp = pileup[:]
			temp[0] = 100 #we're going to roll this to the front, and eventually set that position to zero
			temp = np.roll(np.array(temp), -1)
			stop =[]
			for i, j in zip(temp, np.array(pileup)):
				if i >0:
					stop.append(round((i-j)/i ,4))
				else:
					stop.append(int(0))
			#stop = np.round( (temp - np.array(pileup)) / temp, 4)
			stop[-1] = 0 #Set first (3 prime) postion to zero to avoid infinate start rate

			#write all the data points
			for a,b,c,d,e,f,g,h,i,j,k,l in zip(position, base, pileup, mutation_rate, stop, count_A, count_C, count_G, count_T, count_N, count_del, count_ins):
				pass
				file.write("\n")
				file.write(name+"\t")
				file.write(str(a)+"\t") #position
				file.write(str(b)+"\t") #base
				file.write(str(c)+"\t") #pileup
				file.write(str(d)+"\t") #mutation_rate
				file.write(str(e)+"\t") #stop_rate
				file.write(str(f)+"\t") #count A
				file.write(str(g)+"\t") #count C
				file.write(str(h)+"\t") #count G
				file.write(str(i)+"\t") #count T
				file.write(str(j)+"\t") #count N
				file.write(str(k)+"\t") #count del
				file.write(str(l)) #count ins





if __name__ == "__main__":
	enhance_wig(in_file, ref_file, out_file)
