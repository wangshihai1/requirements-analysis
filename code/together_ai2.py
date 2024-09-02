import os
from together import Together
from predicte import *
import matplotlib.pyplot as plt
from datetime import datetime
import openai
import spacy

client = openai.OpenAI(
  api_key=os.environ.get("TOGETHER_API_KEY"),
  base_url="https://api.together.xyz/v1",
)

#再用一个ai来判断两条语句是否语义相同
judger = openai.OpenAI( 
  api_key=os.environ.get("TOGETHER_API_KEY"),
  base_url="https://api.together.xyz/v1",
)
nlp = spacy.load("en_core_web_sm") 

question1 = ''
with open('../is_equal.txt','r',encoding='utf-8') as f:
    for line in f:
        question1 = question1 + line

def get_formatted_time():
    # 获取当前时间
    now = datetime.now()

    # 格式化当前时间为字符串
    formatted_time = now.strftime('%Y-%m-%d_%H-%M-%S')
    
    return formatted_time

def write_log(begin_time,end_time,accuracy,path):
    with open(path,'a',encoding='utf-8') as f :
        
        f.write(f"* question : question_inEnglish" + '\n')
        f.write('* begin time : ' + begin_time + '\n')
        f.write('* end time : ' + end_time + '\n')
        f.write('* accuracy : ' + str(accuracy) + '\n')
        f.write('------------------------------------' + '\n')
        f.write('\n')
    
def remove_useless_msg(predicte_label):
    for i in range(9):
        label = label_decode[i]
        if label in predicte_label:
            return label
        
def check(sentence1, sentence2): 
    
    stream = judger.chat.completions.create(
        model = model_name,
        messages = [{"role": "user", 
                    "content": question1 + '\n' + "description 1 : " + sentence1 + '\n' + "description 2 : " + sentence2
                    }],
        stream = True,
    )
        
    judge_result = ''
    for chunk in stream:
        judge_result  = judge_result + chunk.choices[0].delta.content
    print(f"sentence1 : {sentence1}")
    print(f"sentence2 : {sentence2}")
    print(f"judge_result : {judge_result}")
    print("-----------------------------")
    return judge_result

begin_time = get_formatted_time()
print(f"begin time : {begin_time}")

TP = [0 for i in range(9)] # 真正例数：实际类别为 i 的样本被正确预测为 i 的数量。
FN = [0 for i in range(9)] # 假负例数：实际类别为 i 的样本被错误预测为其他类别的数量。
FP = [0 for i in range(9)] # 假正例数：实际类别不为 i 但被预测成 i 的样本数量




sentences = []
real_labels = []

question = ''
with open('../question_in_English2.txt','r',encoding='utf-8') as f:
    for line in f:
        question = question + line

full_sentences = open("../new_data.txt",'r',encoding='utf-8').read().split('\n')

for sentence in full_sentences:
    sentences.append(sentence.split('@')[1])
    real_labels.append(trans_trend(sentence.split('@')[2]))

# models = ['google/gemma-2-27b-it', 'allenai/OLMo-7B-Instruct', 'Austism/chronos-hermes-13b', 'deepseek-ai/deepseek-coder-33b-instruct', 'meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo', 'openchat/openchat-3.5-1210']
models = ['allenai/OLMo-7B-Instruct', 'Austism/chronos-hermes-13b', 'deepseek-ai/deepseek-coder-33b-instruct', 'meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo', 'openchat/openchat-3.5-1210']

model_name = "openchat/openchat-3.5-1210"
print(f"正在测试的模型是：{model_name}")

cnt = 0
i = 0
for sentence in sentences:
    print(f"test case : {i + 1}")
    stream = client.chat.completions.create(
        model = model_name,
        messages = [{"role": "user", 
                    "content": question + '\n' + sentence
                    }],
        stream = True,
    )
    
    predicte_label = ''
    for chunk in stream:
        predicte_label  = predicte_label + chunk.choices[0].delta.content
    
    
    
    if "Yes" in check(label_msg[real_labels[i]], predicte_label) :
        cnt += 1
        # print("Yes")
    # if check(label_msg[real_labels[i]], predicte_label):
    #     cnt += 1
    #     id = label_encode[predicte_label]
    #     TP[id] += 1
    # else :
    #     if predicte_label in label_encode : 
            
    #         id = label_encode[real_labels[i]] #实际类别为 i的样本被错误预测为其他类别
    #         FN[id] += 1
    #         id = label_encode[predicte_label]
    #         FP[id] += 1        
        
    i += 1
    

accuracy = cnt / len(sentences)
print(f"accuracy : {accuracy}")
end_time = get_formatted_time()
print(f"end time : {end_time}")  
model_name = model_name.split('/')[0]
write_log(begin_time, end_time, accuracy, f'../预测结果/语言模型API/runtime_{model_name}_log.txt')
exit(0)
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
plt.savefig(f'../可视化/nlp-question-inEnglish/label-recalls(by nlp model)_{model_name}.png')
plt.close()  

plt.figure()
plt.bar(x, precisions, color = 'red') #绘制每一类别数量的柱状图
plt.title('label precisions')
plt.xlabel('label')
plt.ylabel('precision')
plt.savefig(f'../可视化/nlp-question-inEnglish/label-precisions(by nlp model)_{model_name}.png')
plt.close()  

plt.figure()
plt.bar(x, F1_scores, color = 'yellow') #绘制每一类别数量的柱状图
plt.title('label F1_scores')
plt.xlabel('label')
plt.ylabel('F1_score')
plt.savefig(f'../可视化/nlp-question-inEnglish/label-F1_scores(by nlp model)_{model_name}.png')
plt.close()  
        



#