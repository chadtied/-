import requests
import json
import openai
from openai import OpenAI

client= OpenAI(api_key= 'sk-proj-6veP75k5i8ADJ2NMLRoBT3BlbkFJyuZgpZZfcmsPDYjb207C')



file = client.files.create(
  file=open("./law/TPDV,107,重勞訴,46,20200110,1.json", "rb"),
  purpose='assistants'
)
thread= client.beta.threads.create(
    messages=[
    {
      "role": "user",
      "content": "抓取裁判書中 原告起訴主張 和 被告抗辯略以段落 並做法律行為摘要",
      "attachments": [
        { "file_id": file.id, "tools": [{"type": "file_search"}] }
      ],
    }
  ]
)

assistant = client.beta.assistants.create(
  name="Law Assistant",
  instructions="你是法律專家，使用繁體中文，不給予輸出解釋或說明",
  model="gpt-4-turbo-preview",
  tools=[{"type": "file_search"}],
  temperature= 0.2,
)

run = client.beta.threads.runs.create_and_poll(
    thread_id=thread.id, assistant_id=assistant.id
)

messages = list(client.beta.threads.messages.list(thread_id=thread.id, run_id=run.id))

message_content = messages[0].content[0].text
annotations = message_content.annotations

# 將註解文字替換為引用標記
for a, annotation in enumerate(annotations):
    message_content.value = message_content.value.replace(annotation.text,'')

# 輸出處理後的訊息內容
print(message_content.value)


response = client.chat.completions.create(
    model= "gpt-4-turbo-preview",  # 使用您想要的模型
    messages=[
         {"role":"system", "content":"你是法律專家，使用繁體中文。"},
        {"role": "user", "content": f"文件內容如下：\n\n{message_content}\n\n取出此兩點特徵值 案件爭點、原告要求法院判決 (特徵為專有名詞或法律名詞 不顯示金額或法條)，不給予輸出解釋或說明"}
        ],
    temperature= 0.7,
    stream= True,
)

for chunk in response:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")
