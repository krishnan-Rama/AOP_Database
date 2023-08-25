#!/usr/bin/env python

### ------ MIE (mie.db) database ------ ###

import sqlite3
import requests

# Fetch data from the API
response = requests.get("https://aopwiki.org/events.json")
data = response.json()

# Connect to SQLite database (will be created if not exist)
conn = sqlite3.connect('mie.db')

# Create a cursor object
c = conn.cursor()

# Create table
c.execute('''
    CREATE TABLE events
    (id integer, title text, short_name text, biological_organization_id integer, 
    biological_organization_term text, url text)
''')

# Iterate over the data items
for item in data:
    # If biological_organization is None, use default values
    if item['biological_organization'] is None:
        bio_org_id = None
        bio_org_term = None
    else:
        bio_org_id = item['biological_organization']['id']
        bio_org_term = item['biological_organization']['term']

    # Insert a row of data
    c.execute("INSERT INTO events VALUES (?,?,?,?,?,?)",
              (item['id'], item['title'], item['short_name'],
               bio_org_id, bio_org_term, item['url']))


# Save (commit) the changes
conn.commit()

# Close the connection
conn.close()

