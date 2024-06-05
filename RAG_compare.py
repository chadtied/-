from transformers import BertModel, BertTokenizer
import torch
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# 加载BERT模型和tokenizer（中文）
model_name = 'bert-base-chinese'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

# 设定模型为evaluation模式
model.eval()


# 定義文檔庫和查詢
documents = [
    ["給付薪資等", "退休金給付", "加班費給付"],
    ["職業競業之條款之效力", "損害賠償", "延長工時等"],
    ["返回款項", "違約損害賠償", "無"],
    ["加班費給付", "無", "無"]
]
query = ["給付薪資", "違約損害賠償", "返還款項"]

def feature_to_bert_vector(feature):
    # Step 1: Tokenization
    inputs = tokenizer(feature, return_tensors="pt", padding=True, truncation=True)
    
    # Step 2: Forward pass through BERT
    with torch.no_grad():
        outputs = model(**inputs)
        # 'last_hidden_state' will have the hidden states of all tokens
        # 'pooler_output' will have the representation of CLS token
        # Here, using 'pooler_output' which is BERT's choice for representing the whole sentence
        bert_vector = outputs.pooler_output  # Shape: (batch_size, hidden_size)
    
    return bert_vector

# 将所有特征列表中的特征转换为BERT向量
documents_vectors = []
for doc in documents:
    doc_vectors = []
    for feature in doc:
        bert_vector = feature_to_bert_vector(feature)
        doc_vectors.append(bert_vector)
    documents_vectors.append(doc_vectors)

# 将查询转换为BERT向量
query_vectors = []
for qu in query:
    bert_vector = feature_to_bert_vector(qu)
    query_vectors.append(bert_vector)

# 计算查询与每个文档的相似度
similarities = []
for q_vector in query_vectors:
    sim_scores = []
    for d_vectors in documents_vectors:
        sim1 = cosine_similarity(q_vector.reshape(1, -1), d_vectors[0].reshape(1, -1))
        sim2 = cosine_similarity(q_vector.reshape(1, -1), d_vectors[1].reshape(1, -1))
        sim3 = cosine_similarity(q_vector.reshape(1, -1), d_vectors[2].reshape(1, -1))

        print(sim1[0][0], sim2[0][0], sim3[0][0])
    print('\n')

        #sim_scores.append(sim[0][0])  # 取出相似度矩阵的值
    similarities.append(sim_scores)

# 打印相似度结果
for i, sim_list in enumerate(similarities):
    for j, sim in enumerate(sim_list):
        print(f"查询与文档{i+1}中的特征{j+1}的相似度：{sim}")
