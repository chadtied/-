from seleniumbase import Driver
#from lib2to3.pgen2 import driver
from selenium.webdriver.common.by import By
import random
import json
import time
import os
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def Stealing(driver, content):
    driver.get('https://chatgpt.com/')
    #try:
    WebDriverWait(driver,30,0.5).until(EC.presence_of_element_located((By.ID,"prompt-textarea")))
    textarea= driver.find_element(By.ID ,'prompt-textarea')
    ques= "1.輸出下文詐騙手法類型 ，根據【網路購物詐騙、借款詐騙、親友詐騙、愛情詐騙、工作詐騙、投資詐騙、預付費詐騙、人頭帳戶詐騙、恐嚇詐騙、假客服詐騙、假檢警詐騙、商業電子郵件詐騙、略讀詐騙、釣魚詐騙及駭客詐騙】。2.輸出格式(繁體中文):  此為XXXX詐騙。3.內容:"
    textarea.send_keys(ques+content+'\n')
    time.sleep(random.randint(4,5))
    time.sleep(random.randint(4,5))
    textarea= driver.find_element(By.CSS_SELECTOR ,'div.markdown> p')
    return textarea.text
    #except:
        #print("Error")
        #return "Error"


def Send_to_gpt(driver, data):
    if "犯罪事實" in data:
        if isinstance(data['犯罪事實'], list):  content= data['犯罪事實'][0]
        else:   content= data['犯罪事實']        
        
        classify= ''
        response= Stealing(driver, content)
        if response== "Error":  return False
        
        for  alpa in response[2:]:
            classify+= alpa
            if alpa== "騙": break
        data["詐騙類型"]= classify
        return True
        

Year= ["106"]
file_count= 0
driver= Driver(uc= True, incognito= True, headless= False)

for year in Year:
    folder_path = 'C:/Users/user/Desktop/士林地方檢察署/'+year
    for file in os.listdir(folder_path): #檢查各資料夾中json
        if file.endswith('.json'):  #確定為json
            data_json= folder_path+'/'+file
            with open(data_json, encoding="utf-8") as f:    data= json.load(f)
            if Send_to_gpt(driver, data):
                # 將修改後的數據寫回到 JSON 文件中
                file_count+= 1
                if file_count%9== 0:
                    driver.quit()
                    driver= Driver(uc= True, incognito= False, headless= True)
                    time.sleep(4)
                    
                print("已經完成"+str(file_count)+"筆詐騙類型判斷\n\n")
                with open(data_json, 'w', encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

#print(Stealing(driver, content))
