import os
import json
import pandas as pd

# Define the base directory where the species JSON files are located
species_json_dir = '/home/c23048124/Desktop/REACT_2/my-react-app/public/species_data/go_aop_ev'

# Define the path to the TSV file
aop_ke_mie_ao_path = '/home/c23048124/Desktop/REACT_2/my-react-app/aop_ke_mie_ao.tsv'

# Load the TSV file into a DataFrame
aop_ke_mie_ao_df = pd.read_csv(aop_ke_mie_ao_path, sep='\t', header=0)
aop_ke_mie_ao_df['AOP_ID'] = aop_ke_mie_ao_df['Aop:1'].str.extract(r'(\d+)')
aop_ke_mie_ao_df['Event_ID'] = aop_ke_mie_ao_df['Event:142'].str.extract(r'(\d+)')
aop_ke_mie_ao_df['Event_Type'] = aop_ke_mie_ao_df['KeyEvent'].replace({
    'KeyEvent': 'Key Event',
    'AdverseOutcome': 'Adverse Outcome',
    'MolecularInitiatingEvent': 'Molecular Initiating Event'
})
aop_ke_mie_ao_df['Description'] = aop_ke_mie_ao_df['Hyperplasia, Hyperplasia']
simplified_df = aop_ke_mie_ao_df[['AOP_ID', 'Event_ID', 'Event_Type', 'Description']]

# Function to enrich JSON data
def enrich_json_data(json_data):
    for entry in json_data:
        additional_info = simplified_df[
            (simplified_df['AOP_ID'] == str(entry['AOP_ID'])) &
            (simplified_df['Event_ID'] == str(entry['Event_ID']))
        ]
        if not additional_info.empty:
            entry['Event_Type'] = additional_info.iloc[0]['Event_Type']
            entry['Description'] = additional_info.iloc[0]['Description']
    return json_data

# Iterate through each JSON file in the directory
for filename in os.listdir(species_json_dir):
    if filename.endswith('_aop_event_mapping.json'):
        file_path = os.path.join(species_json_dir, filename)
        
        # Read the current JSON data
        with open(file_path, 'r') as file:
            json_data = json.load(file)
        
        # Enrich the JSON data
        enriched_json_data = enrich_json_data(json_data)
        
        # Write the enriched JSON data back to the file
        with open(file_path, 'w') as file:
            json.dump(enriched_json_data, file, indent=4)

        print(f"Enriched data written to {file_path}")

