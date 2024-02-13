#!/usr/bin/env python

import requests
import time

def submit_blast(query_sequence):
    # URL for the UniProt BLAST API
    blast_url = 'https://rest.uniprot.org/blast/uniprot'
    
    # Prepare the data for the POST request to submit a BLAST job
    data = {
        'query': query_sequence,
        'format': 'json'
    }
    
    # Submit the BLAST job
    response = requests.post(blast_url, data=data)
    
    if response.status_code == 200:
        # If the job was successfully submitted, get the job ID
        job_id = response.json()['jobId']
        print(f"BLAST job submitted successfully. Job ID: {job_id}")
        return job_id
    else:
        print(f"Failed to submit BLAST job: {response.status_code}")
        return None

def check_blast_status(job_id):
    # URL to check the status of a BLAST job
    status_url = f'https://rest.uniprot.org/blast/uniprot/{job_id}'
    
    while True:
        response = requests.get(status_url)
        if response.status_code == 200:
            status = response.json()['status']
            if status == 'FINISHED':
                print("BLAST job finished.")
                return True
            elif status == 'RUNNING':
                print("BLAST job still running. Waiting...")
                time.sleep(10)  # Wait for a bit before checking again
            else:
                print(f"BLAST job status: {status}")
                return False
        else:
            print(f"Failed to check BLAST job status: {response.status_code}")
            return False

def retrieve_blast_results(job_id):
    # URL to retrieve the results of a BLAST job
    results_url = f'https://rest.uniprot.org/blast/uniprot/{job_id}/result?format=json'
    
    response = requests.get(results_url)
    if response.status_code == 200:
        # Process the JSON results as needed
        results = response.json()
        print("BLAST results retrieved successfully.")
        return results
    else:
        print(f"Failed to retrieve BLAST results: {response.status_code}")
        return None

# Example usage
query_sequence = "MFSSIILFFVVSSSSAVYSAPKSQLTLQLYYEGFCPFCHSFVELQLYPGYQKLGDSFLVELVPYGKAVYSKAEDGTVSFNCQHGPSECLLNRIHACAINQKPAQADILKFVYCDLSQSTISNTSKELLGIAQTCAQDSNISFDKITTCINSSLSDELLLKYAHQQEKLQPSLRFVPTIRFNGVYNKTLEDDVRANLVQTVCNLLNDEPSVCNNVLSHKVLPQESTIPKNMFLNN"
job_id = submit_blast(query_sequence)
if job_id:
    if check_blast_status(job_id):
        results = retrieve_blast_results(job_id)
        # Further processing of results here

