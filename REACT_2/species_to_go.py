import gzip
import os
import json

# Define the directory containing the species xref files
species_dir = '/home/c23048124/Desktop/REACT/my-react-app/SPECIES'
# Output directory for individual species' GO term JSON files
output_dir = '/home/c23048124/Desktop/REACT/my-react-app/SPECIES_GO'

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Process each xref file
for species_file in os.listdir(species_dir):
    if species_file.endswith('-xref.tsv.gz'):
        species_name = species_file.replace('-xref.tsv.gz', '').replace('_', ' ')
        output_path = os.path.join(output_dir, f"{species_name.replace(' ', '_')}_go_terms.json")

        # Initialize a list to store GO terms for the species
        go_terms = []

        # Read the gzipped xref file
        with gzip.open(os.path.join(species_dir, species_file), 'rt') as f:
            # Skip the header row
            next(f)
            for line in f:
                parts = line.strip().split('\t')
                if len(parts) > 3 and parts[3].startswith('GO:'):
                    go_terms.append(parts[3])
        
        # Save the GO terms to a JSON file specific to the species
        with open(output_path, 'w') as f:
            json.dump(go_terms, f)

        print(f"Processed {species_name}: {len(go_terms)} GO terms saved to {output_path}")

