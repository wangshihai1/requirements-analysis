import pandas as pd
from predicte import trans_trend

# path = '../emprical-data.xlsx'

# df = pd.read_excel(path)

# h, w = df.shape

# print(h, w)

# with open('../new_data2.txt', 'w', encoding = 'utf-8') as f:

#     for i in range(h) :
#         print(i)
#         if (i < 81): line =str(i + 1) + '@' + df.iloc[i, 1][3:]
#         elif(i < 107): line =str(i + 1) + '@' + df.iloc[i, 1][4:]
#         else: line =str(i + 1) + '@' + df.iloc[i, 1]
        
#         if (i < 106):
#             k = len(line) - 1
#             while(line[k] != ','): k -= 1
#             line = line[: k - 1]
            
#         f.write(line + '\n')
    
#     f.close()
    
# path = '../new_labeled_data2.txt'

# with open('../new_labeled_data3.txt', 'w', encoding = 'utf-8') as g :

#     with open(path, 'r', encoding = 'utf-8') as f:
#         cnt = 1
#         for line in f :
#             line = line.split('@')[1] + '@' + line.split('@')[2]
#             line = str(cnt) + '@' + line
#             g.write(line)
#             cnt += 1
                
#         f.close()
        
#     g.close()

with open('../new_labeled_data4.txt', 'w', encoding = 'utf-8') as g:
    with open('../new_data.txt', 'r', encoding = 'utf-8') as f:
        for line in f:
            l = line.split('@')      
            g.write(l[0] + '@' + l[1] + '@' + trans_trend(l[2]) + '\n')
    f.close()
g.close()