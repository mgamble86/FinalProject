# Purpose:	Obtain an idea of how closely related copepod species are within the genus Caligus.
#			By having an idea of the phylogenetic relationships in this genus, it may help to
#			determine if other observed correlations between species (distribution, host specificity,
#			behavior, etc.) may be partially explained by how closely related the species are.

#so I can use regular expressions
import re
#so I can use pexpect
import pexpect

# Obtain copepod genetic sequences from NCBI in FASTA format

# Reformat data so each title and DNA sequence is on a single, individual line
# Define a function to LINEARIZE SEQUENCES
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

				
# turn data into dictionary with name keys and sequences as values
dna_dict = dict(line_seq("Caligus_seq.fasta"))

# remove unwanted and duplicate sequences
# open new dictionary to fill
nodup = {}
# read each dictionary item and add it to "nodup" dictionary if it's a new sequence.  This will eliminate the duplicate sequences
for name,value in dna_dict.items():
    if value not in nodup.values():
        nodup[name] = value
		
# write the contents of the "nodup"	dictionary into a text file so each name and sequence are on line separated by a tab
for name,value in nodup.items():
            f=open('1.txt','a')
            f.write(name + "\t" + value + "\n")
            f.close()

			
# filter for Cytochrome C mitochondrial sequences only and strip excess title information so only species names and sequences remain

# create output file with object name
outfile = open('2.txt', 'w')

# define a function "strip" that uses reg ex to isolate just the genus and species from the titles
def strip(infile):
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

# define input file
infile = open('1.txt', 'r')
# call function "strip"			
strip(infile)
#close files to write		
infile.close()
outfile.close()

#REMOVE SPACES IN SPECIES NAMES

# create new output file
file2 = open('3.txt', 'w')

# Function to remove spaces in species names
def no_space(file1):
    for line in file1:
        ll = line
		# isolates the genus, space, species and sequence into different objects
        pattern = r'(\w+)(\s)(\w+)\t([ACTG]+)'
        aa = re.search(pattern, str(ll))
        if aa != None:
            aa1 = aa.group(1)
            aa3 = aa.group(3)
            aa4 = aa.group(4)
			# replaces the space with an "_"
            file2.write(str(aa1)+ '_' + str(aa3) + '\t' + str(aa4))
            file2.write('\n')
        else:
            continue

# choose input file			
file1 = open('2.txt', 'r')

# call function "no_space"
no_space(file1)

# CREATE NEXUS FILE

# Pre-block of required information at start of file

output = open('1122.nex', 'a')

# define function "block1" to add taxa and character count information to nexus file
def block1(filename):
    with open(filename) as f:
        numtax = len(f.readlines())
        output.write('begin data;')
        output.write('\n')
        output.write('    dimensions ntax=')
		#automatically determines number of taxa based on the number of lines since each line a new sequence
        output.write(str(numtax))
		#number of characters in each sequence.  I couldn't figure out how to have it count these automatically.  Attempted several methods but they only worked some of the time.
        output.write(' nchar=528;')
        output.write('\n')
        output.write('    format datatype=dna interleave=no gap=-;')
        output.write('\n')
        output.write('    matrix')
        output.write('\n')
		
# Insert Caligus species names and sequences between nexus code blocks
		
def align(filename):
    with open(filename) as f:		
        for line in f:
		    #splits on whitespace
            data = line.split()
			#aligns sequences after 25 characters on each line
            output.write('{0[0]:<25}{0[1]:<528}'.format(data))
            output.write('\n')
		# Analysis block to run mcmc at end of file
        output.write('    ;')
        output.write('\n')
        output.write('end;')
        output.write('\n')
        output.write('\n')
        output.write('begin mrbayes;')
        output.write('\n')
        output.write('mcmc ngen = 20000;')
        output.write('\n')
        output.write('\n')
        output.write('end;')
    output.close()

#Call "block1" function
block1('3.txt')
#Call "align" function	
align('3.txt')

# Send nexus file to Mrbayes for execution

#spawn an interactive MrBayes process
child = pexpect.spawn('mb -i 1122.nex')
child.sendline(r'mcmc') 
child.sendline('no') 
child.expect('MrBayes >') 
print child.before
child.sendline('quit')

# Run sumt and sump analysis in MrBayes
#spawn an interactive MrBayes process
child = pexpect.spawn('mb -i 1122.nex')
#send the command 'execute 1122.nex' to MrBayes
child.sendline('execute 1122.nex')
#send the sumt and sump commands to MrBayes, creates tree data
child.sendline('sumt')
child.expect('MrBayes >') 
print child.before
child.sendline('sump')
child.sendline('quit')


# Use tree data and R to construct phylo-tree
# R code used is as follows:

# library(ape)
# tree <- read.nexus("1122.nex.con.tre")
# plot(tree)