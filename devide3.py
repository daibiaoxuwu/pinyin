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


def listtags(text0,voice,smdict,sgdict,rvdict,voicedict):
    #result = jieba.cut_for_search(text0)        ##搜索引擎模式
    result = jieba.cut(text0)        ##搜索引擎模式
    #result.append('EOF')
    oldwd='BOF'
    
    count=0
    for text in result:
        for i in text:
            if i not in voicedict:
                return smdict,sgdict
                
        if len(text)>1:
            smtext=text[1:]
            smvoice=' '.join(voice[text0.index(text)+1:text0.index(text)+len(text)])#wordtopy(smtext,voicedict)#后面几个字的注音
            print(voice[text0.index(text)+1:text0.index(text)+len(text)],text)
        else:
            smtext=''
            smvoice=''
                    
        if oldwd in smdict:
            if text[0] in smdict[oldwd]:
                if smvoice in smdict[oldwd][text[0]]:
                    bigdict=smdict[oldwd][text[0]][smvoice]        #格式:{'走进':{'科':{'xue':{'学':10,'雪':1},'xue jia':{'学家':2}...(后面没有空格)
                    if smtext in bigdict:
                        bigdict[smtext]+=1
                    else:
                        bigdict[smtext]=1
                else:
                    smdict[oldwd][text[0]][smvoice]={smtext:1}
            else:
                smdict[oldwd][text[0]]={smvoice:{smtext:1}}
        else:
            smdict[oldwd]={text[0]:{smvoice:{smtext:1}}}

        oldwd=text 
        count+=len(text)
    return smdict,sgdict

if __name__ == "__main__":

    #语料句子
    smdict={}
    sgdict={}
    rvdict,voicedict=loadvoice('../拼音汉字表.txt')
    print(listtags(    '小明硕士毕业于中国科学院计算所，后在日本京都大学深造',\
    'xiao ming shuo shi bi ye yu zhong guo ke xue yuan ji suan suo hou zai ri ben jing du da xue shen zao'.split(),\
    smdict,sgdict,rvdict,voicedict))
    input()
    


    with open('../pinyin') as f:
        while True:
            a=f.readline()
            if a=='':
                break
            b=f.readline().split()
            smdict,sgdict=listtags(a[:-1],b,smdict,sgdict,rvdict,voicedict)
            print('one')
    with open('../jiebasm3','wb') as f:
        pickle.dump(smdict,f)
