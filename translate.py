import json

# 假設你有一個 JSON 檔案，名為 data.json
# 先讀取該檔案
with open('c:/Users/chad/counter.json', 'r', encoding='utf-8') as file:
    json_data = file.read()

# 使用 json 模組的 loads 函式將 JSON 資料轉換為 Python 的字典
sort_dict = json.loads(json_data)
sort_dict= sorted(sort_dict, key=lambda x:x[1], reverse= True)
# 現在 data_dict 就是包含 JSON 資料的 Python 字典了
Law_case = json.dumps(dict(sort_dict),  ensure_ascii=False)

# 將 JSON 寫入文件或做其他處理
with open('Law_case.json', 'w', encoding="utf-8") as f:
    f.write(Law_case)
