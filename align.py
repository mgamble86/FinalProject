#align sequences
output = open('dicttest.nex', 'a')

def align(filename):
    with open(filename) as f:
        for line in f:
            data = line.split()    # Splits on whitespace
            output.write('{0[0]:<25}{0[1]:<528}'.format(data))
            output.write('\n')
    output.close()
			
align('dicttest_nospace.txt')