import os
import json
from collections import Counter

folder_path = 'C:/Users/chad/Desktop/108/108'

count= 1
counters= Counter()
class_list= dict()

for folder_name in os.listdir(folder_path):
  #print("案件"+str(count)+" 開始執行!!!\n")
  count+= 1
  key= ''
  with open(folder_path+ '/'+ folder_name, encoding="utf-8") as f:    data= json.load(f)

  if "詐騙類型" in data.keys():
    
    case_id= ''
    for alp in data['起訴書編號']:  case_id+= alp

    for alp in data['詐騙類型']:
      key+= (alp+" ")
    if key in counters:
      counters[key] += 1
      class_list[key].append(case_id)
    else:
      counters[key] = 1
      class_list[key]= list()
      class_list[key].append(case_id)

print(counters)
print(class_list)

# 輸出成 JSON
json_output = json.dumps(dict(class_list),  ensure_ascii=False, indent= 4)

# 將 JSON 寫入文件或做其他處理
with open('./tree_L1.json', 'w', encoding="utf-8") as f:
    f.write(json_output)

  
