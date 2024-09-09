import os  
import pandas as pd

# 定义最终结果文件夹路径  
final_result_clean_dir = 'cleaned_swisstargetpred'  
dataset = pd.read_csv('1_Target_Dataset.csv')  
output_dir = 'cleaned_swisstargetpred_mapped'  # 输出文件夹路径  

# 如果输出文件夹不存在，则创建  
os.makedirs(output_dir, exist_ok=True)  

# 获取dataset蛋白号
protein_ids = dataset['proteins'].tolist()  

# 遍历文件夹中的每个文件  
for file_name in os.listdir(final_result_clean_dir):  
    file_path = os.path.join(final_result_clean_dir, file_name)  
    output_file_name = f"{file_name.replace('.txt', '_mapped.txt')}"  
    output_file_path = os.path.join(output_dir, output_file_name)  

    # 打开并读取文件  
    with open(file_path, 'r') as f, open(output_file_path, 'w') as out_f:  
        for line in f:  
            line = line.strip()
            if line in protein_ids:
                print(line)
                out_f.write(f"{line}\n")
    print(f"Mapped {file_name}")