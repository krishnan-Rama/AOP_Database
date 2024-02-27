import json
import os
import requests

# Define your source and destination directories
source_dir = '/home/c23048124/Desktop/REACT_2/my-react-app/public/species_data/go_aop_ev'  # Source directory
destination_dir = '/home/c23048124/Desktop/REACT_2/my-react-app/public/species_data/go_aop_chem'  # Destination directory

# Function to make an API call and fetch AOP details
def fetch_aop_details(aop_id):
    url = f"https://aopwiki.org/aops/{aop_id}.json"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch data for AOP ID {aop_id}")
        return None

# Enrich each entry function with API call
def enrich_entry(entry):
    aop_details = fetch_aop_details(entry["AOP_ID"])
    if aop_details:
        entry["AOP_Short_Name"] = aop_details.get("short_name", "Not Available")
        stressors = aop_details.get("aop_stressors", [])
        entry["Stressor_Name"] = ", ".join([stressor["stressor_name"] for stressor in stressors]) if stressors else "Not Available"
        
        # Logic to populate "Event" and "Relationships" based on the actual structure of the API response
        entry["Event"] = "Populate based on API structure"  # Adjust according to the API response
        entry["Relationships"] = "Populate based on API structure"  # Adjust according to the API response
    else:
        entry["AOP_Short_Name"] = "Not Available"
        entry["Stressor_Name"] = "Not Available"
    return entry

# Process and enrich all species JSON files
def process_all_species(source_dir, destination_dir):
    for filename in os.listdir(source_dir):
        if filename.endswith('_aop_event_mapping.json'):
            source_file_path = os.path.join(source_dir, filename)
            with open(source_file_path, 'r') as file:
                enriched_data = json.load(file)

            enriched_entries = [enrich_entry(entry) for entry in enriched_data]

            destination_file_path = os.path.join(destination_dir, filename)
            with open(destination_file_path, 'w') as file:
                json.dump(enriched_entries, file, indent=4)

            print(f"Enriched data written to {destination_file_path}")

# Ensure the destination directory exists
os.makedirs(destination_dir, exist_ok=True)

# Process all species files
process_all_species(source_dir, destination_dir)

