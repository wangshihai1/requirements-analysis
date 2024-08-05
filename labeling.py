from load_data import get_data2
import sys

last = int(sys.argv[1])

path = './非功能需求.txt'

save_path = './已标记.txt'

sentences , _ =get_data2(path)

print("数据读取完成")

resutl = []

cnt = 0
with open(save_path, 'a',encoding='utf-8') as f:#注意txt的编码格式
    for sentence in sentences:
        cnt +=1
        if cnt < last: continue
        
        cmd = input(sentence + ' :')
        if cmd == 'n':
            continue
        elif cmd == 'exit':
            f.write('下次开始位置：' + str(cnt) + '\n')
            break
        else:
            line = sentence + '@' + cmd + '\n'
            f.write(line)