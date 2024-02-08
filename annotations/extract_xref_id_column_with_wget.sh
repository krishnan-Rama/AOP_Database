#!/bin/bash

# This script downloads a gzipped TSV file from a provided URL, 
# extracts the fourth column, and saves it to a new file.

# Check for correct usage
if [ "$#" -ne 2 ]; then
    echo "Usage: ./extract_xref_id_column_with_wget.sh <tsv_file_url> <output_tsv>"
    exit 1
fi

# Assign URL and output file arguments to variables
tsv_file_url=$1
output_file=$2

# Use wget to download the TSV file
wget -O temp_input_file.tsv.gz "$tsv_file_url"

# Verify download was successful
if [ $? -ne 0 ]; then
    echo "Download failed."
    exit 1
fi

# Extract the fourth column and save it to the output file
zcat temp_input_file.tsv.gz | cut -f1-4 > "$output_file"

# Clean up the temporary file
rm temp_input_file.tsv.gz

echo "Extraction complete. Output saved to $output_file"

