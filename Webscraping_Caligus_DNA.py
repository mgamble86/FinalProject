#This pulls the desired information from the curled NCBI webpages

!# usr/bin/python

from bs4 import BeautifulSoup

#opens the curled NCBI websites with BeautifulSoup
ncbisite = BeautifulSoup(open('Caligus.html'))
#finds main content pane in html file
main_section = ncbisite.find_all('div', class_='content')
#creates file alldna.txt, makes it writeable, and calls it an object named 'my_file'
my_file = open('alldna.txt', 'w')

#pulls the title and dna code from html file
for div in main_section:
    header = div.find('div', class_='rprtheader')
    block = div.find('div', id='viewercontent1')
    name = header.h1
    dna_block = block.span
    
#this will be added into for loop to write into text file	
my_file.write(str(name))
my_file.write('\t')
my_file.write(str(dna_block))
my_file.write('\n')
my_file.close()