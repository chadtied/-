import torch
import os
import json

folder_path = 'C:/Users/chad/Desktop/勞資案件摘要標記/勞資案件摘要'

train_data= []
test_data= []
count= 0

# Step 1: Prepare the dataset
for folder_name in os.listdir(folder_path):
    with open(os.path.join(folder_path, folder_name), 'r', encoding='utf-8') as f:
      file = json.load(f)
    
    count+= 1
    if  count<= 55:
        train_data.append({})
        train_data[-1]["案件編號"]= file["案件編號"]
        train_data[-1]["特徵值"]= file["勞資爭議種類"].split(' ')
        train_data[-1]["內文"]= file["內文"]
    else:
        test_data.append({})
        test_data[-1]["案件編號"]= file["案件編號"]
        test_data[-1]["特徵值"]= file["勞資爭議種類"].split(' ')
        test_data[-1]["內文"]= file["內文"]
    

json_output = json.dumps(train_data,  indent=4, separators=(',', ': '), ensure_ascii=False)
  # 將 JSON 寫入文件或做其他處理
with open("C:/Users/chad/Desktop/勞資案件摘要標記/train_data.json", 'w', encoding="utf-8") as f:
    f.write(json_output)

json_output = json.dumps(test_data,  indent=4, separators=(',', ': '), ensure_ascii=False)
  # 將 JSON 寫入文件或做其他處理
with open("C:/Users/chad/Desktop/勞資案件摘要標記/test_data.json", 'w', encoding="utf-8") as f:
    f.write(json_output)
