#!/usr/bin/env python

import csv

# Paths to your files
terms_file = 'Agelastica_alni.tsv'
data_file = 'aop_ke_ec.tsv'
output_file = 'matched_sorted.tsv'

# Read the rows from the first file and store the necessary information
with open(terms_file, 'r') as f:
    terms = {}
    for line in f:
        columns = line.strip().split('\t')
        if len(columns) >= 4:  # Ensure there are at least 4 columns
            # Map the 4th column term to its corresponding first 3 columns
            terms[columns[:2]] = columns[:3]

# Function to process and match rows, adding corresponding columns
def process_row(row, terms):
    for term, cols in terms.items():
        if term in row:
            # Remove the matching term from its current position
            row.remove(term)
            # Prepend the corresponding three columns and the term to the row
            return cols + [term] + row
    return None

matched_rows = []

# Read and process the second file
with open(data_file, 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        processed_row = process_row(row, terms)
        if processed_row:
            matched_rows.append(processed_row)

# Sort the matched rows based on the first column (after the added columns, this will be the original term's first corresponding column)
matched_rows.sort(key=lambda x: x[3])  # Sorting by the term itself, which is now at index 3

# Write the matched and sorted rows to a new file
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    for row in matched_rows:
        writer.writerow(row)

print(f"Processed and matched rows have been saved to {output_file}.")

