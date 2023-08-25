#!/usr/bin/env python

import argparse
import sqlite3

# Set up command line argument parsing
parser = argparse.ArgumentParser(description='Query the AOP, MIE and CTD databases.')
parser.add_argument('--aop-title', type=str, help='The title of the AOP to query.')
parser.add_argument('--aop-id', type=int, help='The ID of the AOP to query.')
parser.add_argument('--mie-title', type=str, help='The title of the MIE to query.')
parser.add_argument('--mie-id', type=int, help='The ID of the MIE to query.')
parser.add_argument('--cas-rn', type=str, help='The CasRN to query.')
parser.add_argument('--gene-id', type=str, help='The GeneID to query.')
args = parser.parse_args()

# Connect to the SQLite database for AOPs
conn_aop = sqlite3.connect('aops.db')
c_aop = conn_aop.cursor()

if args.aop_title:
    # Query AOPs by title
    c_aop.execute('SELECT * FROM aops WHERE title=?', (args.aop_title,))
elif args.aop_id:
    # Query AOPs by ID
    c_aop.execute('SELECT * FROM aops WHERE id=?', (args.aop_id,))

rows = c_aop.fetchall()
for row in rows:
    print(row)

# Close the connection to AOPs database
conn_aop.close()

# Connect to the SQLite database for MIEs
conn_mie = sqlite3.connect('mie.db')
c_mie = conn_mie.cursor()

if args.mie_title:
    # Query MIEs by title
    c_mie.execute('SELECT * FROM events WHERE title=?', (args.mie_title,))
elif args.mie_id:
    # Query MIEs by ID
    c_mie.execute('SELECT * FROM events WHERE id=?', (args.mie_id,))

# Fetch all query results and print them
rows = c_mie.fetchall()
for row in rows:
    print(row)

# Close the connection to MIEs database
conn_mie.close()

# Connect to the SQLite database for CTD
conn_ctd = sqlite3.connect('ctd.db')
c_ctd = conn_ctd.cursor()

# If a CasRN is specified, query the database for it
if args.cas_rn:
    c_ctd.execute('SELECT * FROM chemical_interactions WHERE CasRN=?', (args.cas_rn,))
# If a GeneID is specified, query the database for it
elif args.gene_id:
    c_ctd.execute('SELECT * FROM chemical_interactions WHERE GeneID=?', (args.gene_id,))

# Fetch all query results and print them
rows = c_ctd.fetchall()
for row in rows:
    print(row)

# Close the connection to the CTD database
conn_ctd.close()

