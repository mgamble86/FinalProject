

# text editing for DNA sequences and names

#linearize sequences
#sed -e 's/\(^>.*$\)/#\1#/' file.fasta | tr -d "\r" | tr -d "\n" | sed -e 's/$/#/' | tr "#" "\n" | sed -e '/^$/d'

#remove duplicate sequences
#sed -e '/^>/s/$/@/' -e 's/^>/#/' file.fasta | tr -d '\n' | tr "#" "\n" | tr "@" "\t" | sort -u -t $'\t' -f -k 2,2  | sed -e 's/^/>/' -e 's/\t/\n/'

my_file = open('cal_dna.txt', 'a')

def read_fasta(fp):
    name, seq = None, []
    for line in fp:
        line = line.rstrip()
        if line.startswith(">"):
            if name: yield (name, ''.join(seq))
            name, seq = line, []
        else:
            seq.append(line)
    if name: yield (name, ''.join(seq))

with open('Caligus_seq.fasta') as fp:
    for name, seq in read_fasta(fp):
        my_file.write(str(name))
        my_file.write('\t')
        my_file.write(str(seq))
        my_file.write('\n')

my_file.close()