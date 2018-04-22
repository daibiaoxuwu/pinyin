import pickle
import json
import re
from pypinyin import pinyin, lazy_pinyin, Style

def loadvoice(path):
    voicedict={}
    rvdict={}
    with open(path,encoding='gbk') as f:
        a=f.readline()#.encode('gbk')
        while(a!=''):
            b=a.split()
            rvdict[b[0]]=b[1:]
            for c in b[1:]:
                voicedict[c]=b[0]
            a=f.readline()
    return rvdict,voicedict

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

    pinyin=lazy_pinyin(text)
    a=''
    for i in text:
        if i in self.voicedict:
            a+=i
    if len(a)!=len(pinyin):
        return smdict

    for i in range(0,len(text)-1):
        word=text[i]
        word2=text[i+1]
        py1=pinyin[i]
        py2=pinyin[i+1]
        
        if py1 not in smdict: smdict[py1]={}
        if word not in smdict[py1]: smdict[py1][word]={}
        if py2 not in smdict[py1][word]: smdict[py1][word][py2]={}
        if word2 not in smdict[py1][word][py2]:
            smdict[py1][word][py2][word2]=1 
        else:
            smdict[py1][word][py2][word2]+=1 
    return smdict

if __name__ == "__main__":

    #语料句子
    rvdict,voicedict=loadvoice('../拼音汉字表.txt')
    smdict={}
    for _ in range(1,12):
        #text=open('../sina_news/2016-%02d.txt'%_).read()
        for text in open('../sina_news/2016-%02d.txt'%_).readlines():
            smdict=listtags(json.loads(text)['html'],smdict,rvdict,voicedict)
            smdict=listtags(json.loads(text)['title'],smdict,rvdict,voicedict)
        print('one')
    with open('dict2d','wb') as f:
        pickle.dump(smdict,f)

