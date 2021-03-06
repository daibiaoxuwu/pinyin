import pickle
import json


#将句子变为"BOSxxxxxEOS"这种形式
def reform(sentence):
    #如果是以“。”结束的则将“。”删掉
    if sentence.endswith("。"):
        sentence=sentence[:-1]
    #添加起始符BOS和终止符EOS   
    sentence_modify1=sentence.replace("。", "EOSBOS")
    sentence_modify2="BOS"+sentence_modify1+"EOS"
    return sentence_modify2
def listtags(text,smdict):
    for i in range(0,len(text)-1):
        smtext=text[i:i+2]
        word=text[i]
        if word in smdict:
            bigdict=smdict[word]
            if smtext in bigdict:
                bigdict[smtext]+=1
            else:
                bigdict[smtext]=1
        else:
            smdict[word]={smtext:1}
    return smdict

if __name__ == "__main__":

    #语料句子
    smdict={}
    for _ in range(1,12):
        #text=open('../sina_news/2016-%02d.txt'%_).read()
        for text in open('../sina_news/2016-%02d.txt'%_).readlines():
            smdict=listtags(json.loads(text)['html'],smdict)
            smdict=listtags(json.loads(text)['title'],smdict)
        print('one')
    with open('dict2c','wb') as f:
        pickle.dump(smdict,f)

