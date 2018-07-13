#!/usr/bin/env python3

# Original repo: https://github.com/dpryan79/ChromosomeMappings

import argparse
from argparse import RawTextHelpFormatter
import gzip
import fileinput
import warnings

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

# read in dpryan converter file and turns into a dict for conversion
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

# reads in input file
def file_roller(file, converter_file):
	converter_dict = create_conversion_dict(converter_file)
	for line in file:
		line = line.decode('utf-8')
		line = line.split()
		# hard coded to assume chr is first entry
		chr = line[0]
		# convert!
		line_copy = line[0]
		try:
			line[0] = converter_dict[chr]
		except:
			warnings.warn("\nWarning! " + line_copy + " could not be converted! Line being skipped!")
			continue
		if line[0] == '':
			continue
		print('\t'.join(line))

def main():
	args = parser.parse_args()
	file = args.file
	# if ends in gz, assume it is gzip
	if file.name[-2:] == 'gz':
		file = gzip.open(file.name)	
	# other just open it
	else:
		file = open(file.name, 'rb') 
	converter_dict = args.converter
	file_roller(file, converter_dict)

main() 
