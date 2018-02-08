#!/usr/local/Anaconda/envs/py3.4.3/bin/python


import argparse
from argparse import RawTextHelpFormatter
import gzip
import fileinput

# https://github.com/dpryan79/ChromosomeMappings
# https://github.com/dpryan79/ChromosomeMappings/blob/master/GRCm38_gencode2ensembl.txt
#converter=open('/home/mcgaugheyd/git/human_variation_landscape/GRCh38_gencode2ensembl.txt')

parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(description= \
		"""
		Uses dpryan79's git converter files to convert chr notation between different 
		schemes. User needs to supply the proper ChromosomeMapping file 
		(/home/mcgaugheyd/git/ChromosomeMappings) and the file to be converted 
		""",formatter_class=RawTextHelpFormatter)
parser.add_argument('-c','--converter', required=True, \
		help = \
		'Supply ChromosomeMapping file (do not forget path) from /home/mcgaugheyd/git/ChromosomeMappings')
parser.add_argument('-f','--file', required=True, type=argparse.FileType('r'), \
		help = \
		'File to be converted. Assumed that the chr is in the first column of a space separated file')

def create_conversion_dict(converter_file):
	converter_dict = {}
	converter = open(converter_file)
	for line in converter:
		line = line.split()
		try:
			converter_dict[line[0]] = line[1]
		except:
			converter_dict[line[0]] = ''
	return(converter_dict)

def file_roller(file, converter_file):
	converter_dict = create_conversion_dict(converter_file)
	for line in file:
		#line = line.decode('utf-8')
		line = line.split()
		
		chr = line[0]
		line[0] = converter_dict[chr]
		if line[0] == '':
			continue
		print('\t'.join(line))

def main():
	args = parser.parse_args()
	file = args.file
	if file.name[-2:] == 'gz':
		file = gzip.open(file.name)
		file = file.readlines()
		file = [line.decode('utf-8') for line in file]
	else:
		file = file.readlines() 
	converter_dict = args.converter
	file_roller(file, converter_dict)

main() 
