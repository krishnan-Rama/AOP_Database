#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: ./extract_xref_id_column.sh <input_tsv.gz> <output_tsv>"
    exit 1
fi

# Assign input and output file arguments to variables
input_file=$1
output_file=$2

# Extract the fourth column and save it to the output file
zcat "$input_file" | cut -f4 > "$output_file"

echo "Extraction complete. Output saved to $output_file"

