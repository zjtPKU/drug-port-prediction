import os
import requests

# 创建存储文件夹
output_folder = "Native_pdb"
os.makedirs(output_folder, exist_ok=True)
def get_pdb_id_from_uniprot(uniprot_id):
    url = f"https://www.uniprot.org/uniprot/{uniprot_id}.xml"
    response = requests.get(url)
    
    if response.status_code == 200:
        xml_content = response.text
        pdb_ids = []
        
        # 查找 <dbReference> 标签，其中 type="PDB"
        import xml.etree.ElementTree as ET
        root = ET.fromstring(xml_content)
        
        for dbReference in root.findall(".//{http://uniprot.org/uniprot}dbReference[@type='PDB']"):
            pdb_id = dbReference.get('id')
            pdb_ids.append(pdb_id)
        
        return pdb_ids
    else:
        print(f"Failed to retrieve data for UniProt ID: {uniprot_id} (Status code: {response.status_code})")
        return None
    
def download_pdb(uniprot_id):
    # 构建PDB文件的URL
    
    pdb_id = get_pdb_id_from_uniprot(uniprot_id)
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"

    # 发送请求
    response = requests.get(url)

    if response.status_code == 200:
        # 下载PDB文件
        with open(os.path.join(output_folder, f"{pdb_id}.pdb"), 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {pdb_id}.pdb")
    else:
        print(f"Failed to download: {pdb_id}.pdb (Status code: {response.status_code})")

# 示例PDB ID列表


# 遍历每个PDB ID并下载PDB文件
download_pdb("A0A087WUZ3")
