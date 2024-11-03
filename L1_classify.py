import os
import json
from collections import Counter

file_name = 'C:/Users/chad/Desktop/108/tree_L1.json'
folder_path= 'C:/Users/chad/Desktop/108/108'

def Case_num(content):
  case_id= ''
  for alp in content:  case_id+= alp
  return case_id


key= ''
with open(file_name, encoding="utf-8") as f:    data= json.load(f)

#輸入的相關類型
input= "金融卡詐騙 身份盜用 "

if input in data.keys():
    print(data[input])
else:
    print('is new type')


#找出文章犯罪事實做比對
for id in data[input]:
    for file in os.listdir(folder_path):
      with open(folder_path+'/'+file, encoding="utf-8") as f:    document= json.load(f)
      if  Case_num(document['起訴書編號'])== id:
          print(document['犯罪事實'],end= '\n')