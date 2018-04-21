import pickle
import json
import jieba
import jieba.posseg as pseg
import jieba.analyse


#将句子变为"BOSxxxxxEOS"这种形式
def reform(sentence):
    #如果是以“。”结束的则将“。”删掉
    if sentence.endswith("。"):
        sentence=sentence[:-1]
    #添加起始符BOS和终止符EOS   
    sentence_modify1=sentence.replace("。", "EOSBOS")
    sentence_modify2="BOS"+sentence_modify1+"EOS"
    return sentence_modify2

def putdict(word,dic):
    if word in dic:
        dic[word]+=1
    else:
        dic[word]=1

def listtags(text,smdict,sgdict):
    result = jieba.cut_for_search(text)        ##搜索引擎模式
    
    for text in result:
        if len(text)==1:
            putdict(text,sgdict)
        else:
            smtext=text[1:]
            if text[0] in smdict:
                bigdict=smdict[text[0]]
                if smtext in bigdict:
                    bigdict[smtext]+=1
                else:
                    bigdict[smtext]=1
            else:
                smdict[text[0]]={smtext:1}
    return smdict,sgdict

if __name__ == "__main__":

    #语料句子
    smdict={}
    sgdict={}
    for _ in range(1,12):
        #text=open('../sina_news/2016-%02d.txt'%_).read()
        for text in open('../sina_news/2016-%02d.txt'%_).readlines():
            smdict,sgdict=listtags(json.loads(text)['html'],smdict,sgdict)
            smdict,sgdict=listtags(json.loads(text)['title'],smdict,sgdict)
        print('one')
    with open('../jiebasm','wb') as f:
        pickle.dump(smdict,f)
    with open('../jiebasg','wb') as f:
        pickle.dump(sgdict,f)

