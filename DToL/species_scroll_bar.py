# species_scroll_bar.py modifications:

from flask import Flask, jsonify, render_template, request
from helpers import extract_species_names, read_xref_file, read_aop_file, enrich_xref_with_aop_event
import os

app = Flask(__name__)

@app.route('/')
def index():
    return 'Welcome to TRACE: Toxicity Response & AOPs Comprehensive Explorer'

@app.route('/species', methods=['GET'])
def get_species():
    directory_path = '/home/c23048124/Desktop/DToL/SPECIES'  # Update your directory path
    species_names = extract_species_names(directory_path)
    return render_template('species.html', species_names=species_names)

@app.route('/analyze', methods=['POST'])
def analyze_species():
    selected_species = request.form.get('selected_species')
    analysis_type = request.form.get('analysis_type')  # AOP or Event

    directory_path = '/home/c23048124/Desktop/DToL/SPECIES'  # Update your directory path
    species_dir = selected_species.replace(' ', '_')

    species_path = os.path.join(directory_path, species_dir)
    xref_file_path = ""
    for filename in os.listdir(species_path):
        if filename.endswith("-xref.tsv.gz"):
            xref_file_path = os.path.join(species_path, filename)
            break
    else:
        return f"No xref file found for species {selected_species}"

    xref_data = read_xref_file(xref_file_path)
    aop_data = read_aop_file('/home/c23048124/Desktop/DToL/aop_ke_ec.tsv')  # Update with the actual path to your AOP file
    enriched_data = enrich_xref_with_aop_event(xref_data, aop_data, analysis_type)

    return render_template('analysis_results.html', enriched_data=enriched_data, analysis_type=analysis_type, species=selected_species)

if __name__ == '__main__':
    app.run(debug=True)

