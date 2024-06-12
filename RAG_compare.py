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
    ["勞動契約", "工資給付", "工作時間", "獎金給付", "確認勞動契約存在", "工資及獎金支付義務違反"],
    ["員工獎懲準則的適用", "保險業務員管理規則的違反", "執行職務不法侵害賠償責任", "求償權的行使", "撤銷懲戒處分", "賠償損害"],
    ["勞雇關係與委任關係的界定", "不當解雇的成立與否", "撤銷不當處分並回復職務及薪資獎金"],
    ["僱傭契約或委任契約", "合法終止契約", "性騷擾行為", "勞動基準法適用", "性別工作平等法程序要件", "默示合意終止契約", "系爭契約繼續存在"],
    ["違反僱傭契約約定", "不正當競爭", "毀損商譽", "判令被告支付懲罰性違約金"],
    ["勞動契約內容", "約定工資項目", "終止僱傭關係條件", "確認勞動契約內容", "違法解僱"],
    ["是否被告以業務緊縮為由終止勞動契約合法", "認定被告終止勞動契約非法，不生效力"],
    ["勞資爭議", "請假手續", "確診證明文件有效性", "勞動契約終止條件", "勞資爭議調解不成立"]
]
#query = ["是否存在僱傭關係與承攬關係之辨別","勞動條件未依法規給付問題，包括加班費", "國定假日工資", "特別休假", "勞工退休金", "就業保險及終止勞動契約之權益（半個月薪水及資遣費）", "1", "被告補提繳勞工退休金至原告之勞工退休金個人專戶", "2", "發給非自願離職證明", "3", "給付平日加班費", "加給國定假日工資", "特別休假補償", "就業保險未投保之損害賠償", "終止勞動契約當月之半個月薪水及資遣費"]
#query = ["是否解除勞動契約合法", "是否存在不能勝任工作之事由", "是否試用期延長合法", "認定解除勞動契約不當"]
query = ["原告任職期間與工作所得報酬的確認", "加班費及特休未休工資的請求", "勞工退休金個人專戶提繳差額的補提撥", "4", "同一集團不同法人格間的雇傭關係釐清", "5", "薪資總額是否符合勞動基準法之最低標準", "6", "修車代墊款債權及賠償訴外人債權的抵銷主張", "1", "確認原告任職期間及其應得的薪資", "加班費", "特休未休工資", "判令被告給付相關工資差額", "判令被告補提撥勞工退休金個人專戶之差額"]

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
for d_vectors in documents_vectors:
    score= 0
    len= 0
    for q_vector in query_vectors:
        sim= 0
        for d_vecrtor in d_vectors:
            if sim< cosine_similarity(q_vector.reshape(1, -1), d_vectors[0].reshape(1, -1)):
                sim= cosine_similarity(q_vector.reshape(1, -1), d_vectors[0].reshape(1, -1))
        score+= sim
        len+= 1

    similarities.append(score/len)

        #sim_scores.append(sim[0][0])  # 取出相似度矩阵的值

print(similarities)
