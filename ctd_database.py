#!/usr/bin/env python

import csv
import sqlite3

# Define path to csv file
csv_file_path = '/mnt/scratch/c23048124/pipeline_all/CTD.csv'

# Connect to SQLite database or create it
conn = sqlite3.connect('ctd.db')
cursor = conn.cursor()

# Create table
cursor.execute("""
    CREATE TABLE chemical_interactions (
    ChemicalName TEXT,
    ChemicalID TEXT,
    CasRN TEXT,
    GeneSymbol TEXT,
    GeneID TEXT,
    GeneForms TEXT,
    Organism TEXT,
    OrganismID TEXT,
    Interaction TEXT,
    InteractionActions TEXT,
    PubMedIDs TEXT)
""")

# Read CSV file and insert records into the SQLite database
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header row
    cursor.executemany("""
        INSERT INTO chemical_interactions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, csv_reader)

# Commit changes and close the connection to the database
conn.commit()
conn.close()

