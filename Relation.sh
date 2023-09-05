#!/usr/bin/env python

import sqlite3
import requests

# Step 1: Fetch data from API
API_URL = "https://aopwiki.org/relationships.json"
data = requests.get(API_URL).json()

# Step 2: Store data in SQLite database

# Connect to SQLite database (will create if not exists)
conn = sqlite3.connect('aop_relationships.db')
cursor = conn.cursor()

# Create the table "relationships"
cursor.execute("""
    CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY,
        url TEXT NOT NULL
    )
""")

# Insert data into the table
for entry in data:
    cursor.execute("""
        INSERT INTO relationships (id, url)
        VALUES (?, ?)
    """, (entry['id'], entry['url']))

conn.commit()
conn.close()

print("Data has been saved to 'aop_relationships.db'")

