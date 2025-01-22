#! /usr/bin/env python

#change the name of this python script to call this the python code name
#i.e. sam_to_bam.py
#import that argparse package to allow piping through the command line
#define the object "parser" that you will use to define the argument terms when running the function
#add the ouput and input files to parser, then simplify the output using args

import argparse 
import gzip
parser = argparse.ArgumentParser()
parser.add_argument('-o', dest='outfile', default='out.bed.gz',
                    help='output file(default out.bed)')
parser.add_argument('-i', '--input', dest='infile', 
                    help='Input file name (required)')
parser.add_argument('-p', dest='pad', default=0,
                    help='Input amount to pad to end of sequence')
parser.add_argument('-z', dest='gzip', default=False, action = 'store_true',
                    help='Determine whether you want to zip the file, if TRUE, run the zipping, else dont')
args = parser.parse_args()


#change the name of the input to be generic, use the dest names defined in args
if args.gzip:
    if not args.outfile.endswith('.gz'):
        args.outfile = args.outfile + '.gz'
    bed = gzip.open(args.outfile,'wt')
else: 
    bed = open(args.outfile,'w')
with open(args.infile, 'r')as sam:
    #add a spacer to the end of each sequence, need to ensure this is an integer.
    spacer = int(args.pad)
    #remove the lines that start with @ and continue until there is no @
    for line in sam:
        if line.startswith('@'):
            continue
      #SAM files are a string, so you need to split the string
      #the '\t' function will separate according to a tab spacer
        columns = line.split('\t') 
        #if the read is unmapped, chr will be a •, remove these by ignoring
        if columns[2] == '*':
            continue
        #specify which columns contain the information I want
        name = columns[0]
        chrom = columns[2]
        #need to do -1 here as the bed file counter starts at 0, rather than 1, as used in a sam file
        start = int(columns[3])-1 - spacer
        #need to undo the modification that was done at the start
        end = (start+spacer) + (len(columns[9])+spacer)
        quality = columns[4]
        #write to a bed file, specifying which columns in the table I want, 
        #n specifies to copy this for n
        bed.write(f'{chrom}\t{start}\t{end}\t{quality}\n')
bed.close()