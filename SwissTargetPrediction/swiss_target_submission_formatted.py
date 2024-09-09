import os  
import pandas as pd  

# 定义源文件夹路径和输出文件路径  
mapped_result_dir = 'cleaned_swisstargetpred_mapped'  
output_csv_path = 'swiss_submission.csv'  # 输出CSV文件路径  

# 存储LDCP号和其对应的UniProt号的字典  
ldcp_uniprot_mapping = {}  

# 遍历文件夹中的每个文件  
for file_name in os.listdir(mapped_result_dir):  
    if file_name.endswith('_clean_mapped.txt'):  # 只处理以_clean_mapped.txt结尾的文件  
        ldcp_id = file_name.replace('_clean_mapped.txt', '')  # 获取LDCP号  

        file_path = os.path.join(mapped_result_dir, file_name)  
        with open(file_path, 'r') as f:  
            uniprot_numbers = [line.strip() for line in f if line.strip()]  # 读取非空行  

        # 记录LDCP号及其对应的UniProt号  
        ldcp_uniprot_mapping[ldcp_id] = uniprot_numbers  

# 创建一个完整的LDCP号列表  
all_ldcp_ids = [f'LDCP{i}' for i in range(33, 103)]  # 从LDCP33到LDCP102  

# 创建一个DataFrame来存储补充后的结果  
filled_data = []  

# 遍历所有LDCP号  
for ldcp in all_ldcp_ids:  
    if ldcp in ldcp_uniprot_mapping:  
        # 如果存在，填入现有值  
        filled_row = [ldcp] + ldcp_uniprot_mapping[ldcp]  
    else:  
        # 如果不存在，填入LDCP号及空值  
        filled_row = [ldcp] + [''] * 70  # 假设最多70个UniProt号  
    
    filled_data.append(filled_row)  

# 创建新的DataFrame并写入新的CSV文件  
filled_df = pd.DataFrame(filled_data)  
filled_df.to_csv(output_csv_path, index=False, header=False)  

print(f'输出CSV文件已生成: {output_csv_path}')