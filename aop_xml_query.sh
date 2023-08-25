#!/bin/bash

# url="https://aopwiki.org/downloads/aop-wiki-xml.gz"  # URL of the compressed XML file
# query="$1"  # The search query provided as the first argument

# Fetch the compressed XML content using curl, decompress it using gunzip, and then pass it to xmllint
# curl -s "$url" | gunzip | xmllint --format - | grep -i "$query" | sed 's/\t/ /g' | tr -s ' ' | sed 's/ /	/g'


url="https://aopwiki.org/downloads/aop-wiki-xml.gz"  # URL of the compressed XML file
query="$1"  # The search query provided as the first argument

# Fetch the compressed XML content using curl, decompress it using gunzip, and then pass it to xmllint
curl -s "$url" | gunzip | xmllint --format - | grep -i "$query" | \
    awk 'BEGIN { FS = "\t" }
         {
           print "----------------------------------------"
           print "Element Name:", $1
           print "Element Value:", $2
           print "----------------------------------------"
         }'

