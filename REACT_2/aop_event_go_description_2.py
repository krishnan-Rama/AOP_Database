import json
import os

# Define your source and destination directories
source_dir = '/home/c23048124/Desktop/REACT_2/my-react-app/public/species_data/go_aop_ev'  # Source directory
destination_dir = '/home/c23048124/Desktop/REACT_2/my-react-app/public/species_data/go_aop_chem'  # Destination directory
aop_jsons_dir = '/home/c23048124/Desktop/REACT_2/my-react-app/public/species_data/aop_jsons'  # Directory containing downloaded AOP JSON files

# Function to load AOP details from a local file
def load_aop_details(aop_id):
    aop_file_path = os.path.join(aop_jsons_dir, f"{aop_id}.json")
    try:
        with open(aop_file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Local AOP JSON file not found for AOP ID {aop_id}")
        return None

# Enrich each entry function using local AOP JSON files
def enrich_entry(entry):
    aop_details = load_aop_details(entry["AOP_ID"])
    if aop_details:
        entry["AOP_Short_Name"] = aop_details.get("short_name", "Not Available")
        stressors = aop_details.get("aop_stressors", [])
        entry["Stressor_Name"] = ", ".join([stressor["stressor_name"] for stressor in stressors]) if stressors else "Not Available"
        # Remove the placeholders for "Event" and "Relationships" as per your requirement
    else:
        entry["AOP_Short_Name"] = "Not Available"
        entry["Stressor_Name"] = "Not Available"
    # Remove the keys for "Event" and "Relationships" if they are not needed
    entry.pop("Event", None)
    entry.pop("Relationships", None)
    return entry

# Process and enrich all species JSON files using local AOP JSONs
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

# Process all species files using local AOP JSONs
process_all_species(source_dir, destination_dir)

