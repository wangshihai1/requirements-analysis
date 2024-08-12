# python3
# Please install OpenAI SDK first：`pip3 install openai`
from openai import OpenAI
from predicte import *
import spacy
import matplotlib.pyplot as plt
from random import randint
from spacy_test import get_all_sub_tree
from datetime import datetime

def get_formatted_time():
    # 获取当前时间
    now = datetime.now()

    # 格式化当前时间为字符串
    formatted_time = now.strftime('%Y-%m-%d_%H-%M-%S')
    
    return formatted_time

def write_log(begin_time,end_time,accuracy,path):
    with open(path,'a',encoding='utf-8') as f :
        
        f.write('* begin time : ' + begin_time + '\n')
        f.write('* end time : ' + end_time + '\n')
        f.write('* accuracy : ' + str(accuracy))
        f.write('------------------------------------')
        f.write('\n')
        
begin_time = get_formatted_time()
print(f"begin time : {begin_time}")

sentences = []
real_labels = []

question = ''
with open('../question.txt','r',encoding='utf-8') as f:
    for line in f:
        question = question + line


client = OpenAI(api_key="sk-c7e36dd880fe47e1afb1a43de39b718b", base_url="https://api.deepseek.com")


full_sentences = open("../new_data.txt",'r',encoding='utf-8').read().split('\n')

for sentence in full_sentences:
    sentences.append(sentence.split('@')[1])
    real_labels.append(trans_trend(sentence.split('@')[2]))

cnt = 0
i = 0
for sentence in sentences:
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": question + '\n' + sentence},
        ],
        stream=False
    )    
    
    predicte_label = response.choices[0].message.content
    if predicte_label == real_labels[i] :
        cnt += 1
        
    i += 1
    print(f"test case : {i}")
    
accuracy = cnt / len(sentences)
print(f"accuracy : {accuracy}")
end_time = get_formatted_time()
print(f"end time : {end_time}")  
write_log(begin_time, end_time, accuracy, '../预测结果/语言模型API/runtime_log.txt')

# while(1) :
#     question = input("请输入对话：")
#     if question == 'exit':
#         break

#     response = client.chat.completions.create(
#         model="deepseek-chat",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant"},
#             {"role": "user", "content": question},
#         ],
#         stream=False
#     )
    
#     print("")
    
#     print("回复：")
    
#     print("")

#     print(response.choices[0].message.content)
    
#     print("--------------------------------------------------")
#     print("")    
    