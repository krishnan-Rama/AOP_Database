import os
import gzip
import pandas as pd
import json

# Define directories
species_base_dir = '/home/c23048124/Desktop/REACT/my-react-app/SPECIES'
output_base_dir = '/home/c23048124/Desktop/REACT_2/my-react-app/public/species_data/go_aop_ev'
aop_mapping_file = '/home/c23048124/Desktop/REACT_2/my-react-app/public/go_to_aop_event_mapping.json'

# Load the GO to AOP/Event mapping
with open(aop_mapping_file) as f:
    go_to_aop_event_mapping = json.load(f)

# Ensure the output directory exists
if not os.path.exists(output_base_dir):
    os.makedirs(output_base_dir)

# Iterate over each species directory
for species_dir in os.listdir(species_base_dir):
    species_path = os.path.join(species_base_dir, species_dir)
    if os.path.isdir(species_path):
        # Find the xref file within each species directory
        for file in os.listdir(species_path):
            if file.endswith('-xref.tsv.gz'):
                xref_path = os.path.join(species_path, file)
                
                # Process the xref file
                with gzip.open(xref_path, 'rt') as f:
                    df = pd.read_csv(f, sep='\t', header=None)
                    go_terms = df[df[3].str.startswith('GO:')][3].unique().tolist()
                
                # Map GO terms to AOPs and Events while including the GO term itself
                species_aop_events = []
                for go_term in go_terms:
                    mappings = go_to_aop_event_mapping.get(go_term, [])
                    for mapping in mappings:
                        # Add the GO term to each mapping
                        species_aop_events.append({'GO_Term': go_term, **mapping})
                
                # Define output file for the species
                output_file_path = os.path.join(output_base_dir, f"{species_dir}_aop_event_mapping.json")
                with open(output_file_path, 'w') as outfile:
                    json.dump(species_aop_events, outfile, indent=4)
                
                print(f"Processed {species_dir}: {len(species_aop_events)} mappings saved to {output_file_path}")

