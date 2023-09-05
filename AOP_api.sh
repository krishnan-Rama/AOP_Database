#!/bin/bash

# Define the API URL
API_URL="https://aopwiki.org/aops.json"

# Use curl to fetch the data
response=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL")
data=$(curl -s "$API_URL")

# Check if the request was successful (HTTP status code 200)
if [ "$response" -eq 200 ]; then
    echo "$data"
else
    echo "Error $response: Unable to fetch data from $API_URL"
fi

