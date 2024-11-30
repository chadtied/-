from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.model_selection import train_test_split
import pandas as pd
import torch
from datasets import Dataset

# 加载数据
labels= {"網路購物詐騙":0, "借款詐騙":1, "親友詐騙":2, "愛情詐騙":3, "投資詐騙": 4, "恐嚇詐騙": 5}
data = pd.read_csv("C:/Users/user/Downloads/migunder2024nov22/output.csv")  # 替换为你的数据路径
data['label'] = data['label'].map(labels)

# 過濾掉 label 數量小於 2 的資料
label_counts = data['label'].value_counts()
valid_labels = label_counts[label_counts >= 2].index
filtered_data = data[data['label'].isin(valid_labels)]


train_texts, val_texts, train_labels, val_labels = train_test_split(
    filtered_data['text'], filtered_data['label'], test_size=0.2, stratify=filtered_data['label']
)

# 加载预训练的 BERT 分词器
tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")

# 数据预处理
def preprocess_function(examples):
    return tokenizer(examples["texts"], truncation=True, padding=True, max_length=512)

train_dataset = Dataset.from_dict({"texts": train_texts, "labels": train_labels})
val_dataset = Dataset.from_dict({"texts": val_texts, "labels": val_labels})
train_dataset = train_dataset.map(preprocess_function, batched=True)
val_dataset = val_dataset.map(preprocess_function, batched=True)

# 加载 BERT 模型
model = BertForSequenceClassification.from_pretrained("bert-base-chinese", num_labels=len(data['label'].unique()))

# 定义训练参数
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_dir="./logs",
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
    learning_rate=5e-5,
    logging_steps=10,
    save_steps=10,
    load_best_model_at_end=True,
)

# Trainer 类
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    tokenizer=tokenizer,
)

# 开始训练
trainer.train()
