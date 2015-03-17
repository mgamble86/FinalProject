# Purpose:	Obtain an idea of how closely related copepod species are within the genus Caligus.
#			By having an idea of the phylogenetic relationships in this genus, it may help to
#			determine if other observed correlations between species (distribution, host specificity,
#			behavior, etc.) may be partially explained by how closely related the species are.

#so I can use regular expressions
import re

# Obtain copepod genetic sequences from NCBI in FASTA format

# Reformat data so each title and DNA sequence is on a single, individual line

# LINEARIZE SEQUENCES
#create file to hold newly formatted information
def line_seq(filename):
    with open(filename) as seqfile:
        name = ""
        seqs = ""
        for line in seqfile:
            line = line.strip()
            if line.startswith(">"):
                if name != "":
                    yield name, seqs
                    seqs = ""
                name = line.lstrip(">")
            else:
                seqs = seqs + line
				
#turn into dict

dna_dict = dict(line_seq("Caligus_seq.fasta"))

#remove unwanted and duplicate sequences
#open new dict
nodup = {}
#reads each dictionary item and adds it to "nodup" dictionary if new sequene
for name,value in dna_dict.items():
    if value not in nodup.values():
        nodup[name] = value
		
		
for name,value in nodup.items():
            f=open('dicttest.txt','a')
            f.write(name + "\t" + value + "\n")
            f.close()
			
# Cytochrome C mitochondrial sequences only
# Strip excess title information so only species names and sequences remain

infile = open('dicttest.txt', 'r')
outfile = open('dicttest_strip.txt', 'w')

for lines in infile:
    ll = lines
    pattern = r'(^g.*)(Caligus\s\w+)(.+?drial)(\s+)([AC]T[A+|G+|C+|T+]{526})'
    aa = re.search(pattern, str(ll))
	#if finds a match, stores name and sequence in groups 2 and 5
    if aa != None:
        aa2 = aa.group(2)
        aa5 = aa.group(5)
		#writes name and sequence separated by a tab
        outfile.write(str(aa2) + '\t' +str(aa5))
		#puts each species and sequence on a new line
        outfile.write('\n')
	#if no match found, continues to next line	
    else:
        continue

#close files to write		
infile.close()
outfile.close()

#REMOVE SPACES IN SPECIES NAMES
# Function to remove spaces in species names

file2 = open('dicttest_nospace.txt', 'w')

def strip(file1):
    for line in file1:
        ll = line
        pattern = r'(\w+)(\s)(\w+)\t([ACTG]+)'
        aa = re.search(pattern, str(ll))
        if aa != None:
            aa1 = aa.group(1)
            aa3 = aa.group(3)
            aa4 = aa.group(4)
            file2.write(str(aa1)+ '_' + str(aa3) + '\t' + str(aa4))
            file2.write('\n')
        else:
            continue
		
file1 = open('dicttest_strip.txt', 'r')

strip(file1)

# Create nexus file

    

	# Write in blocks of nexus directions
        # Pre-block of required information at start of file
        # Analysis block to run mcmc at end of file
    # Insert Caligus species names and sequences between nexus code blocks
	# Ensure species names and sequences are aligned
#align sequences
output = open('dicttest.nex', 'a')

def align(filename):
    with open(filename) as f:
        for line in f:
            data = line.split()    # Splits on whitespace
            output.write('{0[0]:<25}{0[1]:<528}'.format(data)) #aligns sequences after 25 characters on each line
            output.write('\n')
    output.close()
			
align('dicttest_nospace.txt')

# Send nexus file to Mrbayes for execution
    # Run sumt and sump commands
# Send tree information to R to construct phylo-tree