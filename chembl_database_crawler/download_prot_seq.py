import csv
import requests

def get_uniprot_sequence(uniprot_id):
    url = f"https://www.uniprot.org/uniprot/{uniprot_id}.fasta"
    response = requests.get(url)
    if response.status_code == 200:
        fasta_data = response.text
        sequence = ''.join(fasta_data.splitlines()[1:])
        print(f"Retrieved data for {uniprot_id}")
        return sequence
    else:
        print(f"Failed to retrieve data for {uniprot_id}")
        return None

def process_csv(input_csv, output_csv):
    with open(input_csv, mode='r') as infile, open(output_csv, mode='a', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        writer.writerow(['UniProt ID', 'Sequence']) 
        for row in reader:
            uniprot_id = row[0]
            sequence = get_uniprot_sequence(uniprot_id)
            if sequence:
                writer.writerow([uniprot_id, sequence])

if __name__ == "__main__":
    input_csv = 'input.csv' 
    output_csv = 'output.csv'  
    process_csv(input_csv, output_csv)
