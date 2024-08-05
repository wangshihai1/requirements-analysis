from load_data import lcs , is_num
import numpy as np
languagePatterns=[]
labels=[]

def get_word(s):
    res=[' ']
    for word in s.split(' '):
        if word=='':
            continue
        if is_num(word): 
            if '%' in word: # 特殊处理一下数字中带百分号的情况
                res.append(word[0:-1])
                res.append('%')
                continue
        res.append(word)
    return res

#求一个得分阈值来划分可能的匹配模式
def get_score_threshold(sentence):
    scores=[]
    for pattern in languagePatterns:
        _,score=lcs(sentence,pattern)
        scores.append(score)
    scores=np.array(scores)
    q3 = np.percentile(scores, 99)  #求99%分位数
    return q3
    
def get_punishment_score(loc_delta,len_pattren,score): # 如果远距离间隔匹配会被罚得分
    if loc_delta <= len_pattren: k = 1
    else : k = len_pattren/loc_delta
    return k * score
  
#排序函数  
def key_function(result):
    LCS = result[0]
    pattern = result[1]
    if len(LCS):
        loc_delta = LCS[-1] - LCS[0] + 1
    else : loc_delta = 0
    return (result[3],get_punishment_score(loc_delta, len(pattern) - 1, result[3]),len(pattern))    
    #按照最长公共子序列得分、惩罚得分、pattern规模来排序

#预测一句自然语言的变化趋势
def get_label(sentence): #注意：sentence是一个单词列表
    possible_result=[]
    num=len(languagePatterns)
    for i in range(num):
        pattern=languagePatterns[i]
        LCS,score=lcs(sentence,pattern)
        possible_result.append((LCS,pattern,labels[i],score))
    possible_result=sorted(possible_result, key = key_function, reverse=True)
    
    return possible_result

#找到一句需求描述的数字阈值
def get_number(sequence):
    for word in sequence:
        if word[0].isdigit():
            return word
    return "none"
            
def trans_trend(str):
    if str[0]=='2':a=-1
    else: a=int(str[0])
    if str[1]=='2':b=-1
    else: b=int(str[1])
    return (a,b)

def inv_trend(trend):
    return (trend[0] * -1, trend[1] * -1)

full_languagePatterns = open('new_pattern.txt','r',encoding='utf-8').read().split('\n')

for pattern in full_languagePatterns:
    languagePatterns.append(get_word(pattern.split('$')[0]))
    labels.append(pattern.split('$')[1])


# sentences=[]

# full_sentences = open("非功能需求.txt",'r',encoding='ansi').read().split('\n')

# for sentence in full_sentences:
#     sentences.append(sentence.split('@')[0])

# specials=[]
    
# for sentence in sentences:
#     q3=get_score_threshold(get_word(sentence))
#     if q3<=0.5:
#         specials.append(sentence)
        
# with open("specials.txt",'w',encoding='utf8') as f:
#     for sentence in specials:
#         f.write(sentence+'\n')
#     f.close()

# while True:
#     sentence=input("请输入需求语句：")
#     if sentence == "exit":
#         break
#     possible_result= get_label(get_word(sentence)) 
#     i=1
#     for item in possible_result:
#         print(f"possible result {i}")
#         print(f"matched pattern: {item[1]}")
#         print(f"score: {item[3]}")  
#         print(f"threshold: {get_number(item[0])}")
#         print(f"Changing trend: {trans_trend(item[2])}")
#         print("-----------------------------")
#         print()
#         i+=1
#         if i>5:break
#     LCS,matched_pattern,label=get_label(get_word(sentence))
#     print(LCS,matched_pattern,label)
#     print(get_number(LCS))
    