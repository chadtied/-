from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
import torch
import json
import jieba
import jieba.posseg as pseg
from datasets import Dataset
from opencc import OpenCC
import collections

#結巴設置
st= OpenCC('s2t')
ts= OpenCC('t2s')
jieba.add_word(ts.convert("特休假"), freq=1, tag=None)

#詞頻設置
word_counts = collections.Counter()
high_frequency_words= set()

# 標籤列表
labels = ["勞動契約", "工資", "工時", "加班費", "例假及休息日", "休假", "週休二日出勤工作",
          "特別休假", "請假", "女工", "職業災害補償", "工作年資", "契約之終止事由",
          "資遣費", "退休金"]

# 讀取 JSON 文件
with open('C:/Users/chad/Desktop/勞資案件摘要標記/data_set.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

#詞頻紀錄
def word_frequency():
    word_counts = collections.Counter()
    # 遍歷每個文本，進行分詞並計算詞頻
    for text in data:
        words = jieba.lcut(text['內文'], cut_all=False)
        word_counts.update(words)
    print(word_counts)
    # 設置詞頻過濾的閾值，比如過濾掉頻率大於 100 的詞
    frequency_threshold = 100
    high_frequency_words.update({word for word, count in word_counts.items() if count > frequency_threshold})



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

# 將文本轉換成 BERT 所需的格式
def preprocess_function(examples):
    # 使用 jieba.posseg 進行斷詞和詞性標註
    tokenized_text = []
    
    for text in examples['text']:
        words = pseg.lcut(ts.convert(text))  # 斷詞並進行詞性標註
        filtered_words = [word for word, flag in words if flag.startswith('n')]  # 過濾名詞(n)和動詞(v)
        joined_text = st.convert(' '.join(filtered_words))  # 將過濾後的詞彙拼接成字符串
        tokenized_text.append(joined_text)
    
    # 將過濾並處理後的文本轉換為 BERT 所需的格式
    return tokenizer(tokenized_text, padding='max_length', truncation=True, max_length=128)


encoded_dataset = dataset.map(preprocess_function, batched=True)

# 定義 BERT 模型
class BertForMultiLabelSequenceClassification(BertForSequenceClassification):
    def __init__(self, config):
        super().__init__(config)
        self.config.num_labels = config.num_labels
    
    def forward(self, input_ids=None, attention_mask=None, token_type_ids=None, labels=None):
        outputs = super().forward(input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids)
        logits = outputs.logits
        loss = None
        if labels is not None:
            loss_fct = torch.nn.BCEWithLogitsLoss()
            loss = loss_fct(logits, labels.float())
        return (loss, logits) if loss is not None else logits

model = BertForMultiLabelSequenceClassification.from_pretrained('bert-base-chinese', num_labels=len(labels))

# 設定訓練參數
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    weight_decay=0.01,
)

# 初始化 Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=encoded_dataset['train'],
    eval_dataset=encoded_dataset['test'],
)

# 開始訓練
trainer.train()

# 評估模型
eval_results = trainer.evaluate()

print(eval_results)

def predict(text):
    # 使用 jieba 進行斷詞
    tokenized_text = []
    words = pseg.lcut(ts.convert(text))  # 斷詞並進行詞性標註
    filtered_words = [word for word, flag in words if flag.startswith('n')]  # 過濾名詞(n)和動詞(v)
    joined_text = st.convert(' '.join(filtered_words))  # 將過濾後的詞彙拼接成字符串
    tokenized_text.append(joined_text)
    print(tokenized_text)
    inputs = tokenizer(tokenized_text, return_tensors="pt", padding=True, truncation=True, max_length=128)
    with torch.no_grad():
        logits = model(**inputs)[0]  # 直接获取 logits
    predictions = torch.sigmoid(logits).detach().numpy().flatten()  # Flatten to 1D array
    return [label for i, label in enumerate(labels) if predictions[i] > 0.35]

# 使用模型進行預測
new_text = "在這份判決書中提及的勞資權益包括工資給付平日超時工作加班費國定假日及例假日應休未休工資特休假應休未休工資資遣費按勞基法第17條及勞退條例第12條規定的資遣費勞工退休金：依勞退第31條規定的補提繳勞工退休金勞工保險：被告未為原告投保勞工保險，原告自行加入工會投保所支出之保險費這些權益的爭議主要涉及工資、資遣費、勞工退休金的給付以及勞工保險的投保問題。"
predicted_labels = predict(new_text)
print(predicted_labels)
