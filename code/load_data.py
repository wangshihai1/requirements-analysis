import pandas as pd
from random import randint
from sentence_transformers import SentenceTransformer,util
import numpy as np

word_num = {
    'one':'1',
    'two':'2',
    'three':'3',
    'four':'4',
    'five':'5',
    'six':'6',
    'seven':'7',
    'eight':'8',
    'nine':'9',
    'ten':'10'
}


#读取数据集及其标签
def get_data2(path): 
    sentences=[]
    labels=[]
    # 打开文件
    with open(path, 'r',encoding='ansi') as f:#注意txt的编码格式
        # 逐行读取文件内容
        for line in f:

            # 移除行末的换行符并按逗号分割
            items = line.strip().split('@')
            if len(items)<2:
                print(items[0])
                print(i)
                continue
            sentence=items[0]
            label=items[1]
            sentences.append(sentence)
            labels.append(label)


        return sentences,labels


#划分训练集和测试集
def random_move(path,path1,path2):
    train_sentences=[]
    test_sentences=[]
    # 打开文件
    with open(path, 'r',encoding='ansi') as f:#注意txt的编码格式
        # 逐行读取文件内容
        for line in f:
            sign = randint(0,2)
            if(sign<2):
                train_sentences.append(line)

            else :
                test_sentences.append(line)

    with open(path1, 'w',encoding='ansi') as file1:
        for line in train_sentences:
            file1.write(line)  
        
    with open(path2, 'w',encoding='ansi') as file2:
        for line in test_sentences:
            file2.write(line)              

#读取一篇txt里面所有的句子
def get_data4(path):
    sentences=[]     
    with open(path, 'r',encoding='ansi') as f:#注意txt的编码格式 
        for line in f:
            if line.endswith("\n"): line=line[-1]
            print(line)
            sentences.append(line)
             
    return sentences
    
#用于修饰的情态动词
qualifier=["shall","must","shuold","will", "be able to","have", "can"]
add_words=["","not","be"]

#获取所有的语言模式
def extend(languagePatterns):
    res=[]
    cnt=0
    for pattern in languagePatterns:  
        if len(pattern)==0:
            continue
        sentence=pattern.split('$')[0]
        labels=pattern.split('$')[1]
        for word in qualifier:
            for add_word in add_words:
                
                if add_word == "not":
                    label=labels.split(' ')[1]
                else: label=labels.split(' ')[0]
                
                res.append(sentence + " " + word + " " + add_word +" $"+ label)
                res.append(word + " " + add_word + " " + sentence +" $"+ label)
        cnt+=1
    return res

def is_num(x):
    return x[0].isdigit()

def get_hash():
    hash={}
     #读取语言模式
    languagePatterns=open('languagePattern.txt','r',encoding='utf-8').read().split('\n')
    for pt in languagePatterns:
        words=pt.split(' ')
        for word in words:
            hash[word]=1
    for word in qualifier:
        hash[word]=1
    for word in add_words:
        hash[word]=1

    return hash

#获取符合神经网络格式的输入输出数据
def get_data5(path):
    sentences,labels=get_data2(path)
    output=[]
    for label in labels:
        label=label.split(' ')
        x=[]
        for i in label:
            if (i == '') : continue
            x.append(int(i))
        x=np.array(x)    
        output.append(x)
    print("数据、标签加载完成")
    
    #读取语言模式
    languagePatterns=open('languagePattern.txt','r',encoding='utf-8').read().split('\n')
    full_languagePatterns=extend(languagePatterns)
    
    #加载模型
    model = SentenceTransformer("all-MiniLM-L12-v2")
    print("模型加载完成")
    
    #encode
    sentence_embeddings = model.encode(sentences)
    languagePattern_embeddings=model.encode(full_languagePatterns)
    
    
    print("词嵌入完成")
    
    input=[]
    for st_emb in sentence_embeddings:
        similarity=[]
        for lp_emb in languagePattern_embeddings:

            cossim = util.cos_sim(st_emb,lp_emb) #计算句向量和标签向量的余弦相似度
            similarity.append(cossim.item()) #存放在一个列表中，注意cossim函数的返回值是一个tensor张量，需要提取其数值
        similarity=np.array(similarity)
        input.append(similarity) #保存特征向量
    
    print("特征向量计算完成")   
        
    # 将输入列表转换为NumPy数组
    input = np.array(input)    
    output = np.array(output) 
    
    return input,output

#判断两个字符串是否相等
def equal(a,b): 
    
    # 大写变小写
    a = a.lower()
    b = b.lower()
    
    # 数字单词变数字
    if a in word_num:
        a = word_num[a]
    if b in word_num:
        b = word_num[b]
        
    if(is_num(a) and is_num(b)): #都是数字
        return True
   
    if a in qualifier and b in qualifier: # 都是情态动词
        return True
    
    if a == b :
        return True
    return False

#求最长公共子序列的具体内容
def get_lcs_content(sequence,l,r,trans,LCS):
    if(l==0 or r==0):return
    if(trans[l][r]==1):
        get_lcs_content(sequence,l-1,r-1,trans,LCS)
        LCS.append(sequence[l])
    elif(trans[l][r]==2):
        get_lcs_content(sequence,l-1,r,trans,LCS)
    else: get_lcs_content(sequence,l,r-1,trans,LCS)

#求最长公共子序列中每个单词的位置索引
def get_lcs_location(sequence,l,r,trans,LCS):
    if(l==0 or r==0):return
    if(trans[l][r]==1):
        get_lcs_location(sequence,l-1,r-1,trans,LCS)
        LCS.append(l)
    elif(trans[l][r]==2):
        get_lcs_location(sequence,l-1,r,trans,LCS)
    else: get_lcs_location(sequence,l,r-1,trans,LCS)

#求两个句子的最长公共子序列    
def lcs(list1,list2): 
    n=len(list1)
    m=len(list2)
    dp=[[0 for _ in range(m+1)] for _ in range(n+1)]
    trans=[[0 for _ in range(m+1)] for _ in range(n+1)]

    for i in range(n): dp[i][0] = 1
    for i in range(m): dp[0][i] = 1
    for i in range(1,n):
        for j in range(1,m):
            if equal(list1[i],list2[j]):
                dp[i][j]=dp[i-1][j-1]+1
                trans[i][j]=1
            else: 
                if(dp[i-1][j]>=dp[i][j-1]):
                    trans[i][j]=2
                else:
                    trans[i][j]=3
                dp[i][j]=max(dp[i-1][j],dp[i][j-1])
    x = 0 
    y = 0
    for i in range(n):
        for j in range(m):
            if dp[i][j] > dp[x][y]:
                x = i
                y = j
            
    LCS=[]
    get_lcs_location(list1,x,y,trans,LCS)
    
    return LCS,(dp[n-1][m-1] - 1)/(len(list2) - 1)

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

#排序函数
def key_function(result):
    LCS = result[0]
    pattern = result[1]
    if len(LCS):
        loc_delta = LCS[-1] - LCS[0] + 1
    else : loc_delta = 0
    return (result[3],get_punishment_score(loc_delta, len(pattern) - 1, result[3]),len(pattern))    

#如果远距离间隔匹配会被罚得分
def get_punishment_score(loc_delta,len_pattren,score): 
    if loc_delta <= len_pattren: k = 1
    else : k = len_pattren/loc_delta
    return k * score

# sentence = 'As long as the user has access to the client PC   the system will be available 99 % of the time during the first six months of operation . '
# pattern1 = '100 % of'
# pattern2 = 'be 100'

# LCS1,score1 = lcs(get_word(sentence),get_word(pattern1))
# LCS2,score2 = lcs(get_word(sentence),get_word(pattern2))


# # print("loc_delta : ", LCS[-1] - LCS[0] + 1)
# # print("len_pattern : ",len(pattern))
# # print(pattern)
# # print(get_punishment_score(LCS[-1] - LCS[0] + 1, len(pattern) - 1, score))
# possible_result = []
# possible_result.append([LCS1,get_word(pattern1),'**',score1])
# possible_result.append([LCS2,get_word(pattern2),'**',score2])
# possible_result=sorted(possible_result, key = key_function, reverse=True)
# print(possible_result[0][0])
# # print(LCS)


# #读取语言模式
# languagePatterns=open('languagePattern.txt','r',encoding='utf-8').read().split('\n')
# full_languagePatterns=extend(languagePatterns)
# with open('full_languagePatterns.txt','w',encoding='utf-8') as file:
#         for line in full_languagePatterns:
#             file.write(line+'\n')     
