# python3
# Please install OpenAI SDK first：`pip3 install openai`
from openai import OpenAI
from predicte import *
import matplotlib.pyplot as plt
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

TP = [0 for i in range(9)] # 真正例数：实际类别为 i 的样本被正确预测为 i 的数量。
FN = [0 for i in range(9)] # 假负例数：实际类别为 i 的样本被错误预测为其他类别的数量。
FP = [0 for i in range(9)] # 假正例数：实际类别不为 i 但被预测成 i 的样本数量

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
        id = label_encode[predicte_label]
        TP[id] += 1
    else :
        if not predicte_label in label_encode : continue
        
        id = label_encode[real_labels[i]] #实际类别为 i的样本被错误预测为其他类别
        FN[id] += 1
        id = label_encode[predicte_label]
        FP[id] += 1        
        
    i += 1
    print(f"test case : {i}")
    
accuracy = cnt / len(sentences)
print(f"accuracy : {accuracy}")
end_time = get_formatted_time()
print(f"end time : {end_time}")  
write_log(begin_time, end_time, accuracy, '../预测结果/语言模型API/runtime_log.txt')

recalls = []
precisions = []
F1_scores = []
x = [label_decode[i] for i in range(9)]

for i in range(9):
    if TP[i] + FN[i] == 0: 
        recall = 0
    else : 
        recall = TP[i] / (TP[i] + FN[i])
    if TP[i] + FP[i] == 0:
        precision = 0
    else :
        precision = TP[i] / (TP[i] + FP[i])
     
    if recall + precision == 0:
        F1_score = 0
    else :
        F1_score = 2 * (precision * recall) / (precision + recall)       
        
    precisions.append(precision)
    recalls.append(recall)
    F1_scores.append(F1_score)

plt.figure()
plt.bar(x, recalls, color = 'green') #绘制每一类别数量的柱状图
plt.title('label recalls')
plt.xlabel('label')
plt.ylabel('recall')
plt.savefig(f'../可视化/label-recalls(by nlp model).png')
plt.close()  

plt.figure()
plt.bar(x, precisions, color = 'red') #绘制每一类别数量的柱状图
plt.title('label precisions')
plt.xlabel('label')
plt.ylabel('precision')
plt.savefig(f'../可视化/label-precisions(by nlp model).png')
plt.close()  

plt.figure()
plt.bar(x, F1_scores, color = 'yellow') #绘制每一类别数量的柱状图
plt.title('label F1_scores')
plt.xlabel('label')
plt.ylabel('F1_score')
plt.savefig(f'../可视化/label-F1_scores(by nlp model).png')
plt.close()  
    