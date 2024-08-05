from predicte import *
import spacy
import matplotlib.pyplot as plt
from random import randint
from spacy_test import get_all_sub_tree
from datetime import datetime

nlp = spacy.load("en_core_web_sm")

def is_passive(text):
    negative_keywords = ['no', 'not', 'never', 'nothing', 'none']

    text_lower = text.lower()
    if any(keyword in text_lower for keyword in negative_keywords):
        return True
    return False

def get_formatted_time():
    # 获取当前时间
    now = datetime.now()

    # 格式化当前时间为字符串
    formatted_time = now.strftime('%Y-%m-%d_%H-%M-%S')
    
    return formatted_time

def list2str(ls):
    res = ''
    for word in ls:
        res = res + ' ' + word
    return res

def sentence_split(sentence):
    global doc
    sub_sentences = []
    doc = nlp(sentence)
    for seg_sentence in doc.sents: 
        doc1 = nlp(seg_sentence.text)
        sub_tree = get_all_sub_tree(doc1)
        sub_sentences.extend(sub_tree)
    return sub_sentences

def func1(big_sentence):
    big_sentence = big_sentence.lower()
    possible_result = get_label(get_word(big_sentence)) 
    result = possible_result[0]
    Changing_trend = trans_trend(result[2])
    matched_pattern = result[1]
    score = result[3]
    
    return (Changing_trend,list2str(matched_pattern[1:]),score)

def func2(big_sentence):
        score = 0
        Changing_trend = ''
        matched_pattern = ''
        matched_part = ''
        # big_sentence = big_sentence.lower()
        
        sub_sentences = sentence_split(big_sentence) # 获得该需求语句所有可能的分段
        
        for sentence in sub_sentences:                
            possible_result = get_label(get_word(sentence)) 
            result = possible_result[0]
            if score < result[3]:       
                Changing_trend = trans_trend(result[2])
                
                # if (is_passive(sentence) and not is_passive(list2str(result[1][1:]))) : # 语义反转
                #        Changing_trend = inv_trend(Changing_trend)
                       
                score = result[3]                 
                matched_pattern = result[1]
                matched_part = sentence    
                
        return (Changing_trend,list2str(matched_pattern[1:]),score,matched_part)
    
def trend_to_str(trend):
    return str(trend[0]) + ' ' + str(trend[1])
    
def wirte_to_txt(path,test_case,sentence,score,matched_pattern,matched_seg,predict_trend,really_trend):
    with open(path,'a',encoding='utf-8') as f :
        f.write("* " + test_case + '\n')
        f.write("* requirement description : " + sentence + '\n')
        f.write("* score : " + str(score) + '\n')
        f.write("* matched_part : " + matched_pattern + '\n')
        f.write("* matched_seg : " + matched_seg + '\n')
        f.write("* predict_trend : " + trend_to_str(predict_trend)+ '\n')
        f.write("* really_trend : " + trend_to_str(really_trend) + '\n')
        f.write("-------------------------------------------" + '\n')       
        f.write('\n')


sentences = []
real_labels = []
scores = []
fail_scores = []


full_sentences = open("../new_data.txt",'r',encoding='utf-8').read().split('\n')

for sentence in full_sentences:
    sentences.append(sentence.split('@')[1])
    real_labels.append(trans_trend(sentence.split('@')[2]))
    
    
# with open('../new_data.txt','w',encoding='utf-8') as f:
#     index = 1
#     for sentence in full_sentences:
#         s = sentence.split('@')[0]
#         lb = sentence.split('@')[1]
#         f.write(str(index) + '@' + s + '@' + lb + '\n')
#         index += 1

# exit(0)
i = 0
cnt = 0
true_save_path =  f"../预测结果/预测正确/{get_formatted_time()}.txt"
false_save_path = f"../预测结果/预测错误/{get_formatted_time()}.txt"
for big_sentence in sentences:
    
    test_case = f'test case : {i+1}'
    print(test_case)
    
    Changing_trend,matched_pattern,score ,matched_seg= func2(big_sentence)
            
    if Changing_trend == real_labels[i]:
        cnt += 1
        scores.append(score)
        wirte_to_txt(true_save_path,test_case,big_sentence,score,matched_pattern,matched_seg,Changing_trend,real_labels[i])
    else: 
        fail_scores.append(score)
        wirte_to_txt(false_save_path,test_case,big_sentence,score,matched_pattern,matched_seg,Changing_trend,real_labels[i])
    
    i += 1   
 
    
print(cnt / i)
    
n = len(scores)

x = [i for i in range(n)]

m = len(fail_scores)

fail_x = [i for i in range(m)]


# 绘制并保存第一张图
plt.figure()  # 创建新图
plt.scatter(x, scores,c = 'green')
plt.title('Scatter Plot 1')
plt.xlabel('id')
plt.ylabel('score')
plt.savefig(f'../可视化/score_{get_formatted_time()}.png')
plt.close()  # 关闭当前图

# 绘制并保存第二张图
plt.figure()  # 创建新图
plt.scatter(fail_x, fail_scores,c = 'red')
plt.title('Scatter Plot 2')
plt.xlabel('id')
plt.ylabel('score')
plt.savefig(f'../可视化/fail_score_{get_formatted_time()}.png')
plt.close()  # 关闭当前图