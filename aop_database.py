#!/usr/bin/env python

import sqlite3
import requests

# Fetch data from the API
response = requests.get("https://aopwiki.org/aops.json")
data = response.json()

# Connect to SQLite database (will be created if not exist)
conn = sqlite3.connect('aops.db')

# Create a cursor object
c = conn.cursor()

# Create table
c.execute('''
    CREATE TABLE aops
    (id integer, title text, short_name text, abstract text, url text)
''')

# Iterate over the data items
for item in data:
    # Insert a row of data
    c.execute("INSERT INTO aops VALUES (?,?,?,?,?)",
              (item['id'], item['title'], item['short_name'], item['abstract'], item['url']))

# Save (commit) the changes
conn.commit()

# Close the connection
conn.close()

