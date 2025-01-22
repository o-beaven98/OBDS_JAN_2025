''' input bed files a and b, convert two sam files report intervals - 
1. open the bed file
2. read the bed files into the arguments, pass two arguments, input 1 and input 2
3. determine the overlapping sequence by finding where the sequences coordinates overlap:
         if start of b is on the same chromosome and is value between start/end a, this is an overlap. Then run the other configurations.
4. If overlapping, put the value of a at that point in a new table
5. prevent repeated values of a by adding a break function
6. ensure the loop, when it repeats a, continues to iterate over all values of b, using a seek function.
If sequence in one file is equal to the sequence of the other file at
each position - length of the matching interval needs to be greater than 1.
If there is an overlap, write the sequence of the overlapping read
'''

#! /usr/bin/env python

import argparse 

parser = argparse.ArgumentParser()
parser.add_argument('-o', dest='outfile', default='intersections_u.bed',
                    help='output file(default out.bed)')
parser.add_argument('-i_1', '--input_1', dest='a', 
                    help='Input file name (required)')
parser.add_argument('-i_2', '--input_2', dest='b', 
                    help='Input file name (required)')
parser.add_argument('s', '--stdout', dest='std_out
args = parser.parse_args()

with open(args.a, 'r') as a, open(args.b, 'r') as b, open(args.outfile,'w') as intersect:
    for line_a in a:
        columns_a = line_a.split('\t')
        chrom_a = columns_a[0]
        start_a = int(columns_a[1])
        end_a = int(columns_a[2])
        for line_b in b:
            columns_b = line_b.split('\t')
            chrom_b = columns_b[0]
            start_b = int(columns_b[1])
            end_b = int(columns_b[2])
            if chrom_a == chrom_b and ( 
                (start_b >= start_a and start_b <= end_a) or
                (start_b >= start_a and end_b <= end_a) or
                (end_b <= end_a and end_b >= start_a) or
                (start_a >= start_b and end_a <= end_b)):
                    intersect.write(line_a)
                    break
        b.seek(0)

        
        
            
    