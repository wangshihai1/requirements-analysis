from predicte import *
import spacy
import matplotlib.pyplot as plt
from random import randint
from spacy_test import get_all_sub_tree

nlp = spacy.load("en_core_web_sm")

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

    possible_result = get_label(get_word(big_sentence)) 
    result = possible_result[0]
    Changing_trend = trans_trend(result[2])
    matched_pattern = result[1]
    score = result[3]
    
    return (Changing_trend,list2str(matched_pattern),score)

def func2(big_sentence):
        score = 0
        Changing_trend = ''
        matched_pattern = ''
        matched_part = ''
        
        sub_sentences = sentence_split(big_sentence)
        
        for sentence in sub_sentences:         
            possible_result = get_label(get_word(sentence)) 
            result = possible_result[0]
            if score < result[3]:          
                Changing_trend = trans_trend(result[2])
                score = result[3]                 
                matched_pattern = result[1]
                matched_part = sentence    
        return (Changing_trend,list2str(matched_pattern),score,matched_part)


sentences = []
real_labels = []
scores = []
fail_scores = []


full_sentences = open("已标记.txt",'r',encoding='utf-8').read().split('\n')

for sentence in full_sentences:
    sentences.append(sentence.split('@')[0])
    real_labels.append(trans_trend(sentence.split('@')[1]))

with open("对拍6.txt",'w',encoding='utf-8') as f:

    i = 0
    cnt = 0
    for big_sentence in sentences:
        
        res1,matched_part1,score1 = func1(big_sentence)
        res2,matched_part2,score2 ,matched_seg= func2(big_sentence)
        
        if not res1 == res2 :
            
            f.write(big_sentence + '\n')
            f.write("score1 : " + str(score1) + '\n')
            f.write("score2 : " + str(score2) + '\n')
            f.write("matched_part1 : " + matched_part1 + '\n')
            f.write("matched_part2 : " + matched_part2 + '\n')
            f.write("matched_seg : " + matched_seg + '\n')
            
            f.write("-------------------------------------------" + '\n') 
            
            f.write('\n')