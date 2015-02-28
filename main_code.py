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
my_file = open('cal_dna.txt', 'a')
#define function to read through file and grab titles and sequences
def read_fasta(fp):
    name, seq = None, []
	# for loop to go through each line
    for line in fp:
        line = line.rstrip()
		# find beginning of each title
        if line.startswith(">"):
		# if finds title line, grabs next sequence line
            if name: yield (name, ''.join(seq))
            name, seq = line, []
        else:
		#if sequence lines, appends to end of previous line
            seq.append(line)
    if name: yield (name, ''.join(seq))

# opens FASTA file
with open('Caligus_seq.fasta') as fp:
    # goes through each title and sequence
    for name, seq in read_fasta(fp):
	    # puts each title and sequence, separated by a tab, onto an individual line
        my_file.write(str(name))
        my_file.write('\t')
        my_file.write(str(seq))
        my_file.write('\n')
#Close file so it writes
my_file.close()

#STRIP UNWANTED LINES
	# Caligus genus only

file = open('cal_dna.txt', 'r')

select_dna = open('select_dna.txt', 'a')

for line in file:
    if re.search('Caligus\s\w+', line):
        select_dna.write(str(line))
        select_dna.write('\n')
		
select_dna.close()

	# Cytochrome C mitochondrial sequences only
    # Strip excess title information so only species names and sequences remain

infile = open('select_dna.txt', 'r')
outfile = open('strip_test.txt', 'w')

for lines in infile:
    ll = lines
    pattern = r'(^>.*)(Caligus\s\w+)(.+?drial)(\s+)([AC]T[A+|G+|C+|T+]{526})'
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

file2 = open('name_nospace.txt', 'w')

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
		
file1 = open('strip_test.txt', 'r')

strip(file1)
    

# Remove duplicate sequences
# Create nexus file
    # Write in blocks of nexus directions
        # Pre-block of required information at start of file
        # Analysis block to run mcmc at end of file
    # Insert Caligus species names and sequences between nexus code blocks
    # Ensure species names and sequences are aligned
# Send nexus file to Mrbayes for execution
    # Run sumt and sump commands
# Send tree information to R to construct phylo-tree