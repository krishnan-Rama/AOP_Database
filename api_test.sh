#!/bin/bash

result=$(curl -X GET --header "Accept: */*" "https://aopwiki.org/events.json")
echo "Response from server"
echo $result | python -mjson.tool
exit

#import sys, json, csv

# load JSON data
#data = json.load(sys.stdin)

# specify the output directory and file name
#output_dir = '/mnt/scratch/c23048124/pipeline_all/workdir/aops'
#output_file = 'AOPs.csv'
#output_path = f'{output_dir}/{output_file}'

# open the CSV file
#with open(output_path, 'w', newline='') as csvfile:
    # create a CSV writer
#    writer = csv.writer(csvfile)

    # write the header
#    writer.writerow(['id', 'title', 'short_name'])

    # iterate over the data items
#    for item in data:
        # write the required fields to the CSV
#        writer.writerow([item['id'], item['title'], item['short_name']])
#"




