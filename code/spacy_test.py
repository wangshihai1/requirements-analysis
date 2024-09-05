import spacy
from spacy import displacy


nlp = spacy.load("en_core_web_sm")
tree=[]
doc = nlp('')
    
    
def sub_tree(id):
    global tree
    tree.append(id)
    for child in doc[id].children:
        sub_tree(child.i)


def get_all_sub_tree(doc_):
    
    global doc
    global h
    global tree
    doc = doc_
    
    n = len(doc)
        
    res = []
    
    for i in range(n):
        s = ''
        tree=[]
        sub_tree(i)
        tree = sorted(tree)
        for id in tree:
            s = s + ' ' + doc[id].text
        res.append(s)
            
    return res

# nlp = spacy.load("en_core_web_sm")
# doc = nlp("The response time of general student management tasks shall take no longer than 5 seconds and the response time of schedule generation shall take no longer than 30 seconds.")
# for seg_sentence in doc.sents: 
#     print(seg_sentence.text)
# spacy.displacy.serve(doc,style='dep')
# sub_trees = get_all_sub_tree(doc)

# for sbt in sub_trees:
#     print(sbt)

# res=''
# for token in doc:
#     if token.pos_ == 'NOUN' or token.lemma_ == 'the' or token.pos_ == 'PUNCT':
#         continue
    
#     if token.pos_ == 'ADJ' and not token.tag_ == 'JJR': #只要形容词比较级
#         continue
     
#     res+=token.text+' '
#     # print(token.text,token.pos_,token.tag_)
#     # print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#     #         token.shape_, token.is_alpha, token.is_stop)

# print(res)

# doc =nlp("He went to play basketball.")


# for token in doc:
#     print(token.text,' -> ',token.dep_, 'explain : ',spacy.explain(token.dep_))



