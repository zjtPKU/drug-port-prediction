work_dir = "/Users/zhoujt/Desktop/training-data_v3/results"
result_dir = "/Users/zhoujt/Desktop/training-data_v3/results/final_result"

import os
import pandas as pd
import re

check_list = pd.read_csv('/Users/zhoujt/Desktop/training-data_v3/chembl_results.csv', header=None, index_col=None)
check_list.columns = ['ID', 'CHEMBL_ID']

# Read all the files in the work_dir
files = os.listdir(work_dir)
for file in files:
    if file.endswith(".txt"):
        target_index = file.find("_target")
        if target_index != -1:
            # 提取 "_target" 之前的号码
            number = file[:target_index]
        ID = check_list.loc[check_list['CHEMBL_ID'] == number, 'ID'].values[0]
        print(ID)
        with open(f"{work_dir}/{file}", "r") as f:
            lines = f.readlines()
            for line in lines:
                if "CHEMBL" not in line:
                    match = re.search(r'Page \d+:', line)
                    if match:
                        start_position = match.end()
                        match_uniPortID = line[start_position:].strip()
                        print(match_uniPortID)
                        with open(f"{result_dir}/{ID}.txt", "a") as f:
                            f.write(line)