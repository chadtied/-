import os
import json
from collections import Counter

# 建立counter
record= Counter()


for i in range(1, 13):
    #選擇該月資料夾
    folder_path = 'c:/Users/chad/Desktop/司法判決書/2023'
    if(len(str(i))== 1):    folder_path= folder_path +'0'+ str(i)
    else:   folder_path= folder_path + str(i)
    
    for folder_name in os.listdir(folder_path):
        if os.path.isdir(os.path.join(folder_path, folder_name)):   # 檢查是否是資料夾
            for file in os.listdir(os.path.join(folder_path, folder_name)): #檢查各資料夾中json
                if file.endswith('.json'):  #確定為json
                    data_json= os.path.join(os.path.join(folder_path, folder_name), file)
                    with open(data_json, encoding="utf-8") as f:    data= json.load(f)
                    record[data['JTITLE']]+= 1

        print(folder_name+ " ->COMPLETE")
    
    print('\n', folder_path, " <蒐集成功>")    
# 輸出成 JSON
json_output = json.dumps(dict(record),  ensure_ascii=False)

# 將 JSON 寫入文件或做其他處理
with open('counter.json', 'w', encoding="utf-8") as f:
    f.write(json_output)
                