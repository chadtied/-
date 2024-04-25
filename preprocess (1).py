import os
import json
import zipfile
import re
# import regex as re
from pprint import pprint


def crop_judgment(judgment):
    # init
    result = dict()
    jfull_raw = judgment['JFULL'].splitlines()    
    result['案由'] = judgment['JTITLE']
    result['年份'] = judgment['JYEAR']
    result['字別'] = judgment['JCASE']

    # build patterns
    titles = ['主文', '事實', '理由', '事實及理由', '事實及理由要領']
    titles2 = ['相對人', '被告']
    pattern_title = '^\s*(' + '|'.join(['\s*'.join(title) for title in titles]) + ')\s*$'
    pattern_date = '^\s*中\s*華\s*民\s*國.*年.*月.*日\s*$'

    # divide section
    flag = None
    for num, line in enumerate(jfull_raw):
        if num == 0:
            result['標題'] = []
            result['標題'].append(line)

        # section
        if re.match(pattern_title, line) is not None:
            flag = re.sub('\s', '', line)
            result[flag] = list()
        elif re.match(pattern_date, line) is not None:
            flag = None
            break
        elif flag is not None:
            result[flag].append(line.strip())        
    # 解決沒有主文或理由段落
    if len(result.keys()) < 3:
        flag = None
        for num, line in enumerate(jfull_raw):
            # sections
            if re.match('.\s+.\s+人|原\s+告|上列', line):
                if flag is None:
                    flag = '內文'
                    result[flag] = list()
                continue
            elif re.match(pattern_date, line) is not None:
                flag = None
                break
            elif flag is not None:
                result[flag].append(line)
    return result

def resplit_judgment_into_numbered_list(judgment):
    # init
    result = dict()
    r1  = ('①','②','③','④','⑤','⑥','⑦','⑧','⑨','⑩','⑪','⑫','⑬','⑭','⑮','⑯','⑰','⑱','⑲','⑳')
    r2  = ('⑴','⑵','⑶','⑷','⑸','⑹','⑺','⑻','⑼','⑽','⑾','⑿','⒀','⒁','⒂','⒃','⒄','⒅','⒆','⒇')
    r3  = ('Ⅰ','Ⅱ','Ⅲ','Ⅳ','Ⅴ','Ⅵ','Ⅶ','Ⅷ','Ⅸ','Ⅹ')
    r4  = ('壹、', '貳、', '參、', '叄、', '叁、', '参、', '肆、', '伍、', '陸、', '柒、', '捌、', '玖、', '拾、')
    r5  = ('㈠','㈡','㈢','㈣','㈤','㈥','㈦','㈧','㈨','㈩')
    r6  = ('㊀', '㊁', '㊂', '㊃', '㊄', '㊅', '㊆', '㊇', '㊈', '㊉')
    r7  = ('❶', '❷', '❸', '❹', '❺', '❻', '❼', '❽', '❾', '❿', '⓫', '⓬', '⓭', '⓮', '⓯', '⓰', '⓱', '⓲', '⓳', '⓴')
    r8  = ('⒈', '⒉', '⒊', '⒋', '⒌', '⒍', '⒎', '⒏', '⒐', '⒑', '⒒', '⒓', '⒔', '⒕', '⒖', '⒗', '⒘', '⒙', '⒚', '⒛')
    r9  = ('⓵', '⓶', '⓷', '⓸', '⓹', '⓺', '⓻', '⓼', '⓽', '⓾')
    r10 = ('（一）', '（二）', '（三）', '（四）', '（五）', '（六）', '（七）', '（八）', '（九）', '（十）', '（十一）', '（十二）', '（十三）', '（十四）', '（十五）', '（十六）', '（十七）', '（十八）', '（十九）', '（二十）')
    r11 = ('(一)', '(二)', '(三)', '(四)', '(五)', '(六)', '(七)', '(八)', '(九)', '(十)', '(十一)', '(十二)', '(十三)', '(十四)', '(十五)', '(十六)', '(十七)', '(十八)', '(十九)', '(二十)')
    r12 = ('一、', '二、', '三、', '四、', '五、', '六、', '七、', '八、', '九、', '十、', '十一、', '十二、', '十三、', '十四、', '十五、', '十六、', '十七、', '十八、', '十九、', '二十 ')
    r13 = ('A.', 'B.', 'C.', 'D.', 'E.', 'F.', 'G.', 'H.', 'I.', 'J.', 'K.')
    r14 = ('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.', '10.', '11.', '12.', '13.', '14.', '15.', '16.', '17.', '18.', '19.', '20.')
    r15 = ('甲、', '乙、', '丙、', '丁、', '戊、', '己、', '庚、', '辛、', '壬、', '奎、')

    segment_list = [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15]
    all_segment = r1 + r2 + r3 + r4 + r5 + r6 + r7 + r8 + r9 + r10 + r11 + r12 + r13 + r14 + r15
    titles = ['標題', '年份', '案由', '字別']
    # resplit
    for title, text in judgment.items():
        # 標題、案由
        if title in titles:
            merge = ''.join([re.sub('\s', '', line) for line in text])
            result[title] = merge
        else:
            tmp = ''
            count_segment = 1
            main_segment_title = []
            result[title] = {str(1): []}

            for line in text:
                l = re.sub('\s', '', line)
                # 找到大標題
                if not main_segment_title:
                    for r in segment_list:
                        if l.startswith(r):
                            main_segment_title = r
                            tmp += l
                            break
                    else:
                        tmp += l

                # 已有大類標題
                else:
                    # pop temp to result
                    if l.startswith(main_segment_title):
                        result[title][str(count_segment)].append(tmp)
                        count_segment += 1
                        result[title][str(count_segment)] = []
                        tmp = l
                        # sub_segment = [temp]

                    elif l.startswith(all_segment):
                        result[title][str(count_segment)].append(tmp)
                        tmp = l
                    # push into temp
                    else:
                        tmp += l
            result[title][str(count_segment)].append(tmp)    
    return result

def main():
    total = 0                   # 案件數量
    path = 'C:/Users/chad/law_data/'
    pattern = ['事實', '理由', '事實及理由', '事實及理由要領']
    for doc in os.listdir(path):
        # fliters 抗告案件
        if re.search('抗|高等|最高', doc):continue
        # read json file
        with open(path+doc, encoding= "utf-8") as f:
            json_format = json.load(f)
        total += 1
        
        if(json_format['JTITLE']== "支付命令"):
            judgment = crop_judgment(json_format)
            case_content= resplit_judgment_into_numbered_list(judgment)
            if len(case_content)> 4:
                dump_path = 'C:/Users/chad/data/'
                case_title= json_format['JID']+'.json'
                case= json.dumps(case_content,indent=4,ensure_ascii=False)
                # 將 JSON 寫入文件或做其他處理
                with open(dump_path+case_title, 'w', encoding="utf-8") as f:
                    f.write(case)


    print('total:', total)




if __name__ == '__main__':
    main()