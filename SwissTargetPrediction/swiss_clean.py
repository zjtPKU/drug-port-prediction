import os  
import pandas as pd  

# 定义源文件夹路径和输出文件夹路径  
input_dir = 'swisstargetpred'  
output_dir = 'cleaned_swisstargetpred'  # 存放输出文件的文件夹  

# 如果输出文件夹不存在，则创建  
os.makedirs(output_dir, exist_ok=True)  

# 遍历输入文件夹中的每个CSV文件  
for file_name in os.listdir(input_dir):  
    if file_name.endswith('.csv'):  # 只处理CSV文件  
        file_path = os.path.join(input_dir, file_name)  
        
        # 读取CSV文件  
        df = pd.read_csv(file_path)  
        
        # 筛选Probability*大于0的行  
        filtered_df = df[df['Probability*'] > 0]  
        
        # 提取UniProt ID  
        uniprot_ids = filtered_df['Uniprot ID'].tolist()  
        
        # 生成新的文件名  
        clean_file_name = file_name.replace('.csv', '_clean.txt')  
        clean_file_path = os.path.join(output_dir, clean_file_name)  
        
        # 将UniProt ID写入新的文本文件  
        with open(clean_file_path, 'w') as f:  
            for uniprot in uniprot_ids:  
                f.write(f"{uniprot}\n")  
        
        print(f'生成文件: {clean_file_path}')  

print("所有文件已处理完成。")