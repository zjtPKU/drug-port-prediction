import csv
import os
import pandas as pd

csv_file = '/Users/zhoujt/Desktop/training-data_v3/chembl_results.csv'
df = pd.read_csv(csv_file,header = None, index_col = None, sep = ',')
print(df)
# df.columns = ['ID','CHEMBL_ID']

print(df)