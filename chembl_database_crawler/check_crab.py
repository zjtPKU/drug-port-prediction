import requests

import requests

import requests
import xml.etree.ElementTree as ET

def smiles_to_chembl_id(smiles):
    url = f"https://www.ebi.ac.uk/chembl/api/data/molecule?smiles={smiles}"
    response = requests.get(url)
    
    if response.status_code == 200:
        content_type = response.headers.get('Content-Type')
        if 'application/xml' in content_type:
            try:
                root = ET.fromstring(response.content)
                # 假设ChEMBL ID在<molecule_chembl_id>标签内
                chembl_ids = root.findall('.//molecule_chembl_id')
                if chembl_ids:
                    print("smiles_to_chembl_id_complete")
                    print(chembl_ids[0].text)
                    return chembl_ids[0].text
                else:
                    print("No molecule_chembl_id found in the XML response.")
            except ET.ParseError as e:
                print("Error parsing XML:", e)
                print("Response content:", response.text)
        else:
            print(f"Unexpected Content-Type: {content_type}")
            print("Response content:", response.text)
    else:
        print(f"HTTP request failed with status code {response.status_code}")
        print("Response content:", response.text)
    return None


import requests
import xml.etree.ElementTree as ET

def get_protein_targets_from_chembl(chembl_id):
    url = f"https://www.ebi.ac.uk/chembl/api/data/activity?molecule_chembl_id={chembl_id}"
    response = requests.get(url)
    
    if response.status_code == 200:
        content_type = response.headers.get('Content-Type')
        if 'application/xml' in content_type:
            try:
                root = ET.fromstring(response.content)
                proteins = []
                # 假设activities在<activity>标签内
                for activity in root.findall('.//activity'):
                    target_chembl_id = activity.find('target_chembl_id')
                    print(target_chembl_id)
                    if target_chembl_id is not None:
                        target_url = f"https://www.ebi.ac.uk/chembl/api/data/target/{target_chembl_id.text}"
                        target_response = requests.get(target_url)
                        if target_response.status_code == 200:
                            target_root = ET.fromstring(target_response.content)
                            for component in target_root.findall('.//target_component'):
                                accession = component.find('accession')
                                if accession is not None:
                                    proteins.append(accession.text)
                    # return target_chembl_id
                return proteins
            except ET.ParseError as e:
                print("Error parsing XML:", e)
                print("Response content:", response.text)
        else:
            print(f"Unexpected Content-Type: {content_type}")
            print("Response content:", response.text)
    else:
        print(f"HTTP request failed with status code {response.status_code}")
        print("Response content:", response.text)
    
    return None

# Example SMILES
smiles = "CCO"
chembl_id = smiles_to_chembl_id(smiles)
if chembl_id:
    proteins = get_protein_targets_from_chembl(chembl_id)
    print(proteins)
    if proteins:
        print(proteins)
    else:
        print("No protein targets found.")
else:
    print("SMILES not found in ChEMBL.")
