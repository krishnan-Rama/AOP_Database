#!/usr/bin/env python

import csv

# Paths to your files
terms_file = 'Accipiter_gentilis-xref.tsv'
data_file = 'aop_ke_ec.tsv'
output_file = 'matched_sorted.tsv'

# Read the list of terms from the first file
with open(terms_file, 'r') as f:
    terms = [line.strip() for line in f]

# Function to process and match rows
def process_row(row, terms):
    for term in terms:
        if term in row:
            # Move the matching term to the first position
            row.remove(term)
            return [term] + row
    return None

matched_rows = []

# Read and process the second file
with open(data_file, 'r') as f:
    reader = csv.reader(f, delimiter='\t')
    for row in reader:
        processed_row = process_row(row, terms)
        if processed_row:
            matched_rows.append(processed_row)

# Sort the matched rows based on the first column (the term)
matched_rows.sort(key=lambda x: x[0])

# Write the matched and sorted rows to a new file
with open(output_file, 'w', newline='') as f:
    writer = csv.writer(f, delimiter='\t')
    for row in matched_rows:
        writer.writerow(row)

print(f"Processed and matched rows have been saved to {output_file}.")

