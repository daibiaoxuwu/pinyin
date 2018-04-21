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
def wordtopy(text,voicedict):
    voice=''
    for i in text:
        if i in voicedict:
            voice+=voicedict[i]
            voice+=' '
        else:
            voice+='unk'
            voice+=' '
    return voice


def listtags(text,smdict,sgdict,rvdict,voicedict):
    result = jieba.cut_for_search(text)        ##搜索引擎模式
    
    count=0
    for text in result:
        for i in text:
            if i not in voicedict:
                return smdict,sgdict
                
        if len(text)==1:
            putdict(text,sgdict)
        else:
            smtext=text[1:]
            smvoice=' '.join(voice[count+1:count+len(text)])#wordtopy(smtext,voicedict)#后面几个字的注音
                    
            if text[0] in smdict:
                if smvoice in smdict[text[0]]:
                    bigdict=smdict[text[0]][smvoice]        #格式:{'科':{'xue':{'学':10,'雪':1},'xue jia':{'学家':2}...(后面没有空格)
                    if smtext in bigdict:
                        bigdict[smtext]+=1
                    else:
                        bigdict[smtext]=1
                else:
                    smdict[text[0]][smvoice]={smtext:1}
            else:
                smdict[text[0]]={smvoice:{smtext:1}}
        count+=len(text)
    return smdict,sgdict

if __name__ == "__main__":

    #语料句子
    smdict={}
    sgdict={}
    rvdict,voicedict=loadvoice('../拼音汉字表.txt')
#    print(listtags('小明硕士毕业于中国科学院计算所，后在日本京都大学深造',smdict,sgdict,rvdict,voicedict))
    


    with open('../pinyin') as f:
        while True:
            a=f.readline()
            if a=='':
                break
            b=f.readline()
            smdict,sgdict=listtags(a[:-1],b[:-1],smdict,sgdict,rvdict,voicedict)
            print('one')
    with open('../jiebasm2','wb') as f:
        pickle.dump(smdict,f)
    with open('../jiebasg2','wb') as f:
        pickle.dump(sgdict,f)
