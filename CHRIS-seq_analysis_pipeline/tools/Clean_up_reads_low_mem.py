import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i") #Input data path
parser.add_argument("-o") #reference file
parser.add_argument("-c") #collapse?
parser.add_argument("-rc") #output reverse complement?

args = parser.parse_args()

in_file = args.i
out_file = args.o

#Define collapse as boolean
if args.c == "True":
    collapse = True
elif args.c =="False":
    collapse = False

#Define rev_comp as boolean
if args.rc == "True":
    rev_comp = True
elif args.rc == "False":
    rev_comp = False

#define a function to take reverse complements
tab = str.maketrans("ACTG", "TGAC") 
def reverse_complement_table(seq):
	return seq.translate(tab)[::-1]

def read_in_seq_data(in_file, out_file, collapse, rev_comp):
    '''
    This function is doing too much work and sure to cause problems later
    1) reads in fasta data
    2) removes barcode
    3) collapses reads by UMI, maybe
    3) strips off UMI
    4) prints out reverse reverse complements, maybe
    '''

    #open the output file here so it overwrites, and so 
    #we don't have to keep opening and closing it.
    with open(out_file, "w") as out:

        #initialize a set to hold unique sequences
        seq_set=set()

        #open data file and start writing lines one at a time
        with open(in_file) as f:
            line = "adsf" #initialize the line variable to start the while loop

    #       loop through the fasta file data
            while line:
                #seq_set=set() #TEST TEST TEST TEST TEST TEST TEST TEST TEST
                #Advance the line reader by 1.
                line = f.readline().strip()


                if line =="":
                    continue #this seems to happend at the end of file
                    #when line should be None, instead it comes back as empty string


                #check to see if its a name or a sequence
                if line[0]==">": #names start with ">"
                    name = line #set new name
                    seq = "" #reset the sequence
                    continue #move on to the next line
                else: #sequences don't start with ">"
                    seq = line

                #if we're collapsing PCR duplicates then we need to
                #maintain a set of unique sequences, and skip repeated sequences
                if collapse:
                    #Check to see if seq in set. If it is, skip, otherwise, add
                    if seq in seq_set:
                        continue #SKIP this read
                    else:
                        seq_set.add(seq) #add to the set
                        output_read((name,seq), out, rev_comp)

                #if we're not collapsing the read, then just write output
                else:
                    output_read((name, seq), out, rev_comp)


def output_read(read_tuple, out_file, rev_comp):
    name = read_tuple[0]
    seq = read_tuple[1]

    #Trim the read
    seq = str(seq[:-6]) #TRIM THE UMI off
    seq = seq[7:] #trim off the barcode

    #Reverse complement the read if needed
    if rev_comp:
        seq = reverse_complement_table(seq)

    #Open out file and append these reads
    out_file.write(str(name)+"\n")
    out_file.write(seq+"\n")




#     #Read in the whole damn file
#     with open(in_file, "r") as f: #added CK
#         lines = f.readlines()

#     if collapse:
#         #To collapse PCR duplicates (identified by UMI) we'll make a dictionary
#         #keyed by sequence, valued by name
#         read_dict={}
#         read_list=[]
#         for line in lines:
#             if line[0] == ">":
#                 name = line.strip()
#             else:
#                 seq = line.strip()
#                 read_dict[seq]=name #the new dictionary way
#         #dictionary collapsed stuff, now make a list of tuples
#         for seq in read_dict.keys():
#             read_list.append((read_dict[seq], seq))

#     else:
#         #since we're not collpasing duplicates, just make a list of tuples
#         read_dict={}
#         read_list=[]
#         for line in lines:
#             if line[0] == ">":
#                 name = line.strip()
#             else:
#                 seq = line.strip()
#                 read_list.append((name, seq)) #20201026, the old way

#     #With the list of tuples, TRIM OFF THE UMI and write output
#     with open(out_file, "w") as out_file:
#         for read in read_list:
#             seq = read[1]
#             name = read[0]

#             UMI_trimmed_seq = str(seq[:-6]) #TRIM THE UMI off
#             UMI_trimmed_seq = UMI_trimmed_seq[7:] #trim off the barcode

#             #Write output, take reverse complement if the option is true
#             out_file.write(str(name)+"\n")
#             if rev_comp:
#                 out_file.write(reverse_complement_table(UMI_trimmed_seq)+"\n")
#             else:
#                 out_file.write(UMI_trimmed_seq+"\n")

#run the main function based on the input arguments

if __name__ == "__main__":
    read_in_seq_data(in_file, out_file, rev_comp, collapse)
