#!/bin/bash

url="https://aopwiki.org/downloads/aop-wiki-xml.gz"  # URL of the compressed XML file

# Fetch the compressed XML content using curl, decompress it using gunzip, and then pass it to xmllint
curl -s "$url" | gunzip | xmllint --format -

