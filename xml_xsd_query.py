#!/usr/bin/env python3.6

import xml.etree.ElementTree as ET

def find_443_in_xml(xml_file_path):
    # Parse the XML file
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Recursive function to search through the XML elements
    def recursive_search(element):
        if element.text == "443":
            print(f"Found '443' in element <{element.tag}> with value: {element.text}")
        for child in element:
            recursive_search(child)

    # Start the search from the root
    recursive_search(root)

if __name__ == '__main__':
    xml_file_path = '/mnt/scratch/c23048124/databases/aopwiki.xml'
    find_443_in_xml(xml_file_path)
