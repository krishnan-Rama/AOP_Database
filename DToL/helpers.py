import os
import re
import gzip
import csv

def extract_species_names(directory_path):
    species_names = set()
    pattern = re.compile(r'([A-Za-z]+_[A-Za-z]+)')
    for filename in os.listdir(directory_path):
        match = pattern.match(filename)
        if match:
            species_name = match.group(1).replace('_', ' ')
            species_names.add(species_name)
    return sorted(species_names)

def read_xref_file(file_path):
    xref_data = {}
    with gzip.open(file_path, 'rt') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            xref_id = row[3]  # Correctly extracting GO terms from the 4th column
            xref_data[xref_id] = row
    return xref_data

def read_aop_file(file_path):
    # Placeholder for compatibility; actual AOP data processing occurs during enrichment
    return file_path

def enrich_xref_with_aop_event(xref_data, aop_file_path, analysis_type):
    enriched_data = []
    # Prepare AOP data for flexible search
    with open(aop_file_path, 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            for go_term in xref_data.keys():
                if go_term in row:  # If the GO term is found in any column of this row
                    aop_info = row[0] if analysis_type == 'AOP' else row[1]  # Assuming AOP is the first column and Event is the second
                    enriched_data.append((go_term, aop_info))
                    break  # Assuming only one occurrence of each GO term per row
    return enriched_data

