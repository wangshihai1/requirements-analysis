#本模块封装了各种工具函数

from load_data import lcs , is_num
import numpy as np
from spacy_test import get_all_sub_tree
from datetime import datetime
import spacy

languagePatterns=[]
labels=[]
nlp = spacy.load("en_core_web_sm")
negative_words = open('../pattern/negative_word.txt', 'r', encoding = 'utf-8').read().split('\n')

#将句子分割为单词列表
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
 
#根据最长公共子序列的紧凑程度进行罚分   
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
    possible_result = []
    num = len(languagePatterns)
    for i in range(num):
        pattern = languagePatterns[i]
        LCS, score = lcs(sentence,pattern)
        if len(pattern) == 3:
            if len(LCS) > 0:
                score = get_punishment_score(LCS[-1] - LCS[0] + 1, 2, score)
        possible_result.append((LCS, pattern, labels[i], score, i))
    possible_result=sorted(possible_result, key = key_function, reverse=True)
    
    return possible_result

#找到一句需求描述的数字阈值
def get_number(sequence):
    for word in sequence:
        if word[0].isdigit():
            return word
    return "none"

#数字编码转字符串编码           
def trans_trend(s):
    if s[0]=='2':a=-1
    else: a=int(s[0])
    if s[1]=='2':b=-1
    else: b=int(s[1])
    return str(a) + ' ' + str(b)

#暴力匹配（可用kmp优化）一个句子中是否包含某个短语
def match(sentence1, sentence2):
    n = len(sentence1)
    m = len(sentence2)
    for i in range(1, m) :
        j = 1
        k = i
        while(j < n and k < m and sentence1[j] == sentence2[k]):
            j += 1
            k += 1
        if j == n : return True
        
    return False

#检测语义反转
def is_passive(text): #text是一个单词列表
    text = get_word(text)
    for keyword in negative_words :
        if match(get_word(keyword), text):
            return keyword
    return 'no negative word'

#获取当前时间
def get_formatted_time():
    now = datetime.now()

    # 格式化当前时间为字符串
    formatted_time = now.strftime('%Y-%m-%d_%H-%M-%S')
    
    return formatted_time

#将一列表中的词汇拼接成字符串
def list2str(ls):
    res = ''
    for word in ls:
        res = res + ' ' + word
    return res

#写日志
def wirte_to_txt(path, test_case, sentence, score, matched_pattern, matched_seg, predict_trend, really_trend, negative_word):
    with open(path,'a',encoding='utf-8') as f :
        f.write("* " + test_case + '\n')
        f.write("* requirement description : " + sentence + '\n')
        f.write("* score : " + str(score) + '\n')
        f.write("* matched_part : " + matched_pattern + '\n')
        f.write("* matched_seg : " + matched_seg + '\n')
        f.write("* predict_trend : " + predict_trend + '\n')
        f.write("* really_trend : " + really_trend + '\n')
        f.write("* negative_word : " + negative_word + '\n')
        f.write("-------------------------------------------" + '\n')       
        f.write('\n')

#将一个句子划分为多个子句，每个子句内部的词汇相关性较高
def sentence_split(sentence):
    global doc
    sub_sentences = []
    doc = nlp(sentence)
    for seg_sentence in doc.sents: 
        doc1 = nlp(seg_sentence.text)
        sub_tree = get_all_sub_tree(doc1)
        sub_sentences.extend(sub_tree)
    return sub_sentences        

full_languagePatterns = open('../pattern/pattern4.txt','r',encoding='utf-8').read().split('\n')

for pattern in full_languagePatterns:
    languagePatterns.append(get_word(pattern.split('$')[0]))
    labels.append(pattern.split('$')[1])
    

