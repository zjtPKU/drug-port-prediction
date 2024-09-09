#!/bin/bash  

# 设置要上传的文件夹  
SMILES_DIR="./smiles"  
# 设置输出文件夹
RESULTS_DIR="./results"
# 设置目标URL  
TARGET_URL="http://swisssimilarity.ch:1234/startscreen?library=CHEMBL&method=Combined"  
# 设置会话检索URL  
RETRIEVE_URL="http://swisssimilarity.ch:1234/retrievesession"  
# 设置会话检查URL  
CHECK_URL="http://swisssimilarity.ch:1234/checksession"  

# 创建结果文件夹  
mkdir -p "$RESULTS_DIR"  

# 遍历每个.smi文件并进行上传  
for smi_file in "$SMILES_DIR"/*.smi; do  
    # 确保文件存在  
    if [ -e "$smi_file" ]; then  
        echo "Uploading $smi_file ..."  
        
        # 使用 curl 上传文件  
        response=$(curl -s -F "mySMILES=@$smi_file" "$TARGET_URL")  

        # 打印响应  
        echo "Response: $response"  
    else  
        echo "No .smi files found in the directory."  
    fi  

    # 检查工作状态
    status_response=""  
    while [ "$status_response" != "Calculation is finished" ]; do  
    	sleep 5  # 每 5 秒检查一次  
        status_response=$(curl -s "$CHECK_URL?sessionNumber=$response")  
        echo "Current status: $status_response"       
    done  
    
    # 检索会话结果并保存到文件中
    result_response=$(curl -s "$RETRIEVE_URL?sessionNumber=$response")
    result_file="$RESULTS_DIR/${smi_file##*/}.result.txt"
    echo "$result_response" > "$result_file" 
    echo "Results saved to $result_file"
done  

echo "Completed."
