import re

#def DNA_dict(filename):
#    all_seqs = []
#    with open(filename) as seqfile:
#        name = ""
#        seqs = ""
#        for line in seqfile:
#            line = line.strip()
#            if line.startswith(">"):
#                if name != "":
#                    all_seqs.append([name, seqs])
#                    seqs = ""
#                name = line.lstrip(">")
#            else:
#                seqs = seqs + line
#    return all_seqs 

#all_seqs = rem_dups("Caligus_seq.fasta")
	

def parse_fasta2(filename):
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

dna_dict = dict(parse_fasta2("Caligus_seq.fasta"))

#remove unwanted and duplicate sequences
#open new dict
result = {}
#remove duplicate sequences
for name,value in dna_dict.items():
    if value not in result.values():
        result[name] = value
for name,value in result.items():
            f=open('dicttest.txt','a')
            f.write(name + "\t" + value + "\n")
            f.close()

			
#file = open('dicttest.txt', 'r')

#select_dna = open('dicttest_calonly.txt', 'a')

#for line in file:
#    if re.search('Caligus\s\w+', line):
#        select_dna.write(str(line))
#        select_dna.write('\n')
		
#select_dna.close()

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