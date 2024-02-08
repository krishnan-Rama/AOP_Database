#!/usr/bin/env python

import pandas as pd
import gzip

def parse_fasta_gz(filepath):
    """Parse a gzipped FASTA file and return a dictionary mapping IDs to sequences."""
    sequences = {}
    sequence_id = None
    sequence = []

    with gzip.open(filepath, 'rt') as file:  # 'rt' mode for reading as text
        for line in file:
            line = line.strip()
            if not line:
                continue
            if line.startswith('>'):  # new sequence
                if sequence_id is not None:
                    sequences[sequence_id] = ''.join(sequence)
                sequence_id = line[1:].split()[0]  # get the first part of the ID
                sequence = []
            else:
                sequence.append(line)

        # Add the last sequence
        if sequence_id is not None:
            sequences[sequence_id] = ''.join(sequence)

    return sequences

def map_sequences_to_tsv(fasta_file, tsv_file, output_file):
    """Map sequences from a gzipped FASTA file to the first column of a TSV based on IDs in the third column."""
    # Parse the gzipped FASTA file to get the sequences
    fasta_sequences = parse_fasta_gz(fasta_file)

    # Adjust the mapping to remove ".1" from the end of the IDs in the FASTA sequences
    adjusted_fasta_sequences = {key.rsplit('.', 1)[0]: value for key, value in fasta_sequences.items()}

    # Load the TSV file
    matched_sorted_df = pd.read_csv(tsv_file, sep='\t', header=None)

    # Map the sequences from adjusted_fasta_sequences to matched_sorted_df based on the IDs in the third column
    matched_sorted_df[0] = matched_sorted_df[2].map(adjusted_fasta_sequences)

    # Save the updated dataframe to a new TSV file
    matched_sorted_df.to_csv(output_file, sep='\t', index=False, header=False)

    return matched_sorted_df

# Define file paths
fasta_file = 'Agelastica_alni-GCA_950111635.1-2023_07-pep.fa.gz'
tsv_file = 'matched_sorted.tsv'
output_file = 'updated_matched_sorted_with_sequences.tsv'

# Run the mapping function
updated_df = map_sequences_to_tsv(fasta_file, tsv_file, output_file)

# Display the first few rows of the updated dataframe to verify
print(updated_df.head())

