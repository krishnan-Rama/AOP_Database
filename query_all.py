#!/usr/bin/env python

import argparse
import sqlite3

# Set up command line argument parsing
parser = argparse.ArgumentParser(description='Query the AOP, MIE and CTD databases.')
parser.add_argument('--search', type=str, help='The text to search for in all text fields.')
args = parser.parse_args()

databases = ['aops.db', 'mie.db', 'ctd.db']
tables = {'aops.db': ['aops'], 'mie.db': ['events'], 'ctd.db': ['chemical_interactions']}  

for db in databases:
    conn = sqlite3.connect(db)
    c = conn.cursor()

    for table in tables[db]:
        # Get the column names
        c.execute(f'PRAGMA table_info({table});')
        columns = [row[1] for row in c.fetchall()]
        
        for column in columns:
            query = f"SELECT * FROM {table} WHERE {column} LIKE ?"
            c.execute(query, ('%' + args.search + '%',))
            
            rows = c.fetchall()
            for row in rows:
                print(row)

    conn.close()

