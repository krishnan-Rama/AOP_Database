#!/usr/bin/env python

import argparse
import sys

def construct_url(pep_id, query_type, file_path):
    with open(file_path, 'r') as file:
        for line in file:
            columns = line.strip().split('\t')
            if columns[2] == pep_id:
                for col in columns:
                    if col.startswith(query_type.capitalize() + ":"):
                        identifier = col.split(":")[1]
                        return f"https://wikikaptis.lhasacloud.org/#/{query_type}/{identifier}/viewer"
    return None

def main():
    parser = argparse.ArgumentParser(description="Query for AOP or KE URLs by peptide ID.")
    parser.add_argument("--type", choices=['aop', 'ke'], required=True, help="The type of query (aop or ke).")
    parser.add_argument("--pep-id", required=True, help="The peptide ID to query.")
    args = parser.parse_args()

    file_path = 'updated_matched_sorted_with_sequences.tsv'  # Path to your TSV file
    url = construct_url(args.pep_id, args.type, file_path)
    
    if url:
        print(url)
    else:
        print(f"No matching {args.type.upper()} found for peptide ID {args.pep_id}", file=sys.stderr)

if __name__ == "__main__":
    main()

