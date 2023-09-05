#!/usr/bin/env python3.6

module load python/3.10.5

pip install xmlschema
import xml.etree.ElementTree as ET
import sqlite3
from xmlschema import XMLSchema

# Load XSD schema
xsd = XMLSchema('aopwiki.xsd')

# Parse XML file
tree = ET.parse('aopwiki.xml')
root = tree.getroot()

# Create SQLite database
conn = sqlite3.connect('aopwiki.db')
cursor = conn.cursor()

# Generate SQL schema based on XSD
create_table_statements = []
for element_name, element_type in xsd.maps.types.items():
    if element_type.is_simple():
        create_table_statements.append(f'{element_name} {element_type.primitive_type()}')

create_table_query = f'CREATE TABLE Data ({", ".join(create_table_statements)})'
cursor.execute(create_table_query)
conn.commit()

# Insert data into the database
for item in root:
    values = [item.find(element_name).text if element_name in item else '' for element_name in xsd.maps.types.keys()]
    insert_query = f'INSERT INTO Data VALUES ({", ".join(["?"] * len(values))})'
    cursor.execute(insert_query, values)

conn.commit()
conn.close()

