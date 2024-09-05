from tools import *
from static_data import *
import matplotlib.pyplot as plt

#核心函数，求各种预测信息
def predicte(big_sentence):
        score = 0
        Changing_trend = ''
        matched_pattern = ''
        matched_part = ''
        negative_word = 'no negative word'
        big_sentence = big_sentence.lower()
        
        # sub_sentences = sentence_split(big_sentence) # 获得该需求语句所有可能的分段 
        # for sentence in sub_sentences:
        # sentence = sentence.lower() 
                       
        possible_result = get_label(get_word(big_sentence)) 
        
        if possible_result[0][4] == 0: # 和 100 % of 匹配
            if possible_result[0][0][0] == possible_result[1][0][-1]: #对 100 % of 进行修饰
                possible_result[0] = possible_result[1] #修饰语为大
     
                print("wsh: " + big_sentence)
                print(possible_result[0][1])
                print(possible_result[1][1])
                print("------------------")
                print("")
  
        result = possible_result[0]
        Changing_trend = result[2]
        negative_word = is_passive(big_sentence)
        if  negative_word != 'no negative word' : # 语义反转
                if result[4] != 0: # 100 % of 不需要语义反转
                    Changing_trend = label_inv[Changing_trend] 
                
        score = result[3]                 
        matched_pattern = result[1]
        matched_part = big_sentence    
                
        return (Changing_trend, list2str(matched_pattern[1:]), score, matched_part, negative_word)
    

begin_time = get_formatted_time()

sentences = []
real_labels = []
scores = []
fail_scores = []
data_path = '../new_labeled_data2.txt'

full_sentences = open(data_path,'r',encoding='utf-8').read().split('\n')

for sentence in full_sentences:
    sentences.append(sentence.split('@')[1])
    label = sentence.split('@')[2]
    real_labels.append(label)
    id = label_encode[label]
    num[id] += 1

i = 0
cnt = 0
true_save_path =  f"../预测结果/预测正确/{get_formatted_time()}.txt"
false_save_path = f"../预测结果/预测错误/{get_formatted_time()}.txt"

for big_sentence in sentences:
    
    test_case = f'test case : {i+1}'
    print(test_case)
    
    Changing_trend, matched_pattern, score, matched_seg, negative_word = predicte(big_sentence)
            
    if Changing_trend == real_labels[i]:
        cnt += 1
        scores.append(score)
        wirte_to_txt(true_save_path,test_case,big_sentence,score,matched_pattern,matched_seg,Changing_trend,real_labels[i], negative_word)
        id = label_encode[Changing_trend]
        TP[id] += 1
    else: 
        fail_scores.append(score)
        wirte_to_txt(false_save_path,test_case,big_sentence,score,matched_pattern,matched_seg,Changing_trend,real_labels[i], negative_word)
        id = label_encode[real_labels[i]] #实际类别为 i的样本被错误预测为其他类别
        FN[id] += 1
        id = label_encode[Changing_trend]
        FP[id] += 1
        
    i += 1   


print("accuracy : ",cnt / i)
    
n = len(scores)

x = [i for i in range(n)]

m = len(fail_scores)

fail_x = [i for i in range(m)]

recalls = []
precisions = []
F1_scores = []

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
    print(f"* recall of label {label_decode[i]} : {recall} ")
    print(f"* number of label {label_decode[i]} : {num[i]}")
    print("-----------------------------------")
    print("")

end_time = get_formatted_time()

print("* begin time : ",begin_time)
print("* end_time : ",end_time)

exit(0)

# 绘制并保存第一张图
plt.figure()  # 创建新图
plt.scatter(x, scores,c = 'green')
plt.title('Scatter Plot 1')
plt.xlabel('id')
plt.ylabel('score')
plt.savefig(f'../可视化/score-distribution/score_{get_formatted_time()}.png')
plt.close()  # 关闭当前图

# 绘制并保存第二张图
plt.figure()  # 创建新图
plt.scatter(fail_x, fail_scores,c = 'red')
plt.title('Scatter Plot 2')
plt.xlabel('id')
plt.ylabel('score')
plt.savefig(f'../可视化/score-distribution/fail_score_{get_formatted_time()}.png')
plt.close()  # 关闭当前图

x = [label_decode[i] for i in range(9)]
plt.figure()
plt.bar(x, num, color = 'blue') #绘制每一类别数量的柱状图
plt.title('label distribution')
plt.xlabel('label')
plt.ylabel('num')
plt.savefig(f'../可视化/label-distribution.png')
plt.close()  # 关闭当前图

plt.figure()
plt.bar(x, recalls, color = 'green') #绘制每一类别数量的柱状图
plt.title('label recalls')
plt.xlabel('label')
plt.ylabel('recall')
plt.savefig(f'../可视化/label-recalls.png')
plt.close()  

plt.figure()
plt.bar(x, precisions, color = 'red') #绘制每一类别数量的柱状图
plt.title('label precisions')
plt.xlabel('label')
plt.ylabel('precision')
plt.savefig(f'../可视化/label-precisions.png')
plt.close()  

plt.figure()
plt.bar(x, F1_scores, color = 'yellow') #绘制每一类别数量的柱状图
plt.title('label F1_scores')
plt.xlabel('label')
plt.ylabel('F1_score')
plt.savefig(f'../可视化/label-F1_scores.png')
plt.close()  