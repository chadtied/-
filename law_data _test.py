import requests
import json
import re
import os
import openai
from openai import OpenAI

client= OpenAI(api_key= '')
folder_path = 'C:/Users/chad/Desktop/實驗組'


for folder_name in os.listdir(folder_path):

  record= list()

  file = client.files.create(
    file=open(os.path.join(folder_path, folder_name), "rb"),
    purpose='assistants'
  )
  thread= client.beta.threads.create(
      messages=[
      {
        "role": "user",
        "content": "抓取裁判書中 原告起訴主張段落 和 被告抗辯略以段落",
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
          {"role": "user", "content": f"文件內容如下：\n\n{message_content}\n\n取出此兩點特徵值 案件爭點、原告要求法院判決 (特徵為法律名詞 不顯示金額或法條)，不給予輸出解釋或說明"}
          ],
      temperature= 0.7,
      stream= True,
  )
  init_respon= str()
  for chunk in response:
      if chunk.choices[0].delta.content is not None:
        init_respon += chunk.choices[0].delta.content

  print(init_respon, end= "\n\n")
  init_respon= init_respon.replace("原告要求法院判決", "")
  init_respon= init_respon.replace("案件爭點", "")
  record+= re.split(r"[：:-、 。.\n\r]", init_respon)

  # 使用 list comprehension 去除空白元素，包括 None
  filtered_record = list(filter(None, [item.strip() if isinstance(item, str) else item for item in record]))
  
  # 輸出成 JSON
  json_output = json.dumps(filtered_record,  ensure_ascii=False)

  # 將 JSON 寫入文件或做其他處理
  with open("./實驗組特徵/gpt_"+folder_name, 'w', encoding="utf-8") as f:
      f.write(json_output)

  
  client.beta.threads.delete(thread_id=thread.id)
  client.files.delete(file.id)
  client.beta.assistants.delete(assistant.id)
