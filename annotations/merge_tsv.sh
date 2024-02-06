#!/bin/bash

# Define file names
file1="Accipiter_gentilis-xref.tsv" # Your first TSV file with just GO terms
file2="aop_ke_ec.tsv" # Your second TSV file with GO terms and associated information

# Sort both files on the first column (if they aren't already sorted)
sort $file1 > file1_sorted.tsv
sort -k1,1 $file2 > file2_sorted.tsv

# Join the files on the first column
join -t $'\t' file1_sorted.tsv file2_sorted.tsv > merged.tsv

