from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
import torch
import json
from datasets import Dataset
from sklearn.model_selection import train_test_split
import jieba

# 標籤列表
labels = ["勞動契約", "工資", "工時", "加班費", "例假及休息日", "休假", "週休二日出勤工作",
          "特別休假", "請假", "女工", "職業災害補償", "工作年資", "契約之終止事由",
          "資遣費", "退休金"]

# 讀取 JSON 文件
with open('C:/Users/chad/Desktop/勞資案件摘要標記/data_set.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 將數據轉換成 Dataset 格式
def labels_to_binary(label_list):
    return [float(1 if label in label_list else 0) for label in labels]

dataset = Dataset.from_dict({
    "text": [item["內文"] for item in data],
    "labels": [labels_to_binary(item["特徵值"]) for item in data]
})

# 切分數據為訓練集和測試集
dataset = dataset.train_test_split(test_size=0.2)


# 加載 BERT 分詞器
tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')

print(tokenizer.tokenize(""))