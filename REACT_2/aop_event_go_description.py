import json
import os
import requests

# Define your source and destination directories
source_dir = '/home/c23048124/Desktop/REACT_2/my-react-app/public/species_data/go_aop_ev'  # Source directory
destination_dir = '/home/c23048124/Desktop/REACT_2/my-react-app/public/species_data/go_aop_chem'  # Destination directory for processed files
aop_jsons_dir = '/home/c23048124/Desktop/REACT_2/my-react-app/public/species_data/aop_jsons'  # Local directory for AOP JSON files

# Ensure directories exist
os.makedirs(destination_dir, exist_ok=True)
os.makedirs(aop_jsons_dir, exist_ok=True)

# Function to fetch or load AOP details
def get_or_fetch_aop_details(aop_id):
    local_file_path = os.path.join(aop_jsons_dir, f"{aop_id}.json")
    if os.path.exists(local_file_path):
        with open(local_file_path, 'r') as file:
            return json.load(file)
    else:
        url = f"https://aopwiki.org/aops/{aop_id}.json"
        response = requests.get(url)
        if response.status_code == 200:
            aop_data = response.json()
            with open(local_file_path, 'w') as file:
                json.dump(aop_data, file, indent=4)
            return aop_data
        else:
            print(f"Failed to fetch data for AOP ID {aop_id}")
            return None

# Enrich each entry
def enrich_entry(entry):
    aop_details = get_or_fetch_aop_details(entry["AOP_ID"])
    if aop_details:
        entry["AOP_Short_Name"] = aop_details.get("short_name", "Not Available")
        stressors = aop_details.get("aop_stressors", [])
        entry["Stressor_Name"] = ", ".join([stressor["stressor_name"] for stressor in stressors]) if stressors else "Not Available"
        # Removed "Event" and "Relationships" fields as they are not populated from the API in this script
    else:
        entry["AOP_Short_Name"] = "Not Available"
        entry["Stressor_Name"] = "Not Available"

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

# Start the process
process_all_species(source_dir, destination_dir)

