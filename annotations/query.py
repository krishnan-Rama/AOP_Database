import argparse
import sys

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Query for AOP or KE links.')
    parser.add_argument('--type', type=str, choices=['aop', 'ke'], required=True,
                        help='The type of link to generate (aop or ke).')
    parser.add_argument('--pep-id', type=str, required=True,
                        help='Peptide ID to search for.')
    return parser.parse_args()

def search_file(pep_id, search_type, file_path):
    """Search the file for the peptide ID and return the corresponding AOP or KE number."""
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            if parts[2] == pep_id:
                if search_type == 'aop':
                    # Assuming Aop identifier is in the 5th column and formatted as Aop:number
                    aop_number = parts[4].split(':')[1]  
                    return aop_number
                elif search_type == 'ke':
                    # Assuming Event identifier is in the 6th column and formatted as Event:number
                    ke_number = parts[5].split(':')[1]  
                    return ke_number
    return None

def generate_link(search_type, number):
    """Generate the corresponding link based on the type and number."""
    base_url = 'https://wikikaptis.lhasacloud.org/#/'
    if search_type == 'aop':
        return f'{base_url}aop/{number}/viewer'
    elif search_type == 'ke':
        return f'{base_url}ke/{number}/viewer'

def main():
    args = parse_arguments()
    file_path = 'updated_matched_sorted_with_sequences.tsv'  # Adjust the file path as needed
    number = search_file(args.pep_id, args.type, file_path)
    if number:
        link = generate_link(args.type, number)
        print(link)
    else:
        print(f'No matching entry found for peptide ID {args.pep_id} and type {args.type}.', file=sys.stderr)

if __name__ == '__main__':
    main()

