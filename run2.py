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

def work(line,smdict,rvdict,voicedict,pointset):

    line=line.split()

    oldlist=rvdict[line[0]]
    oldsent=rvdict[line[0]]
    oldpower=[1]*len(oldlist)
    
    for i in line[1:]:#i 拼音
        newlist=rvdict[i]
        newpower=[0]*len(newlist)
        newsent=['']*len(newlist)
        for j in range(len(newlist)):#j:汉字
            for k in range(len(oldlist)):
                if oldlist[k] in smdict:
                    if i in smdict[oldlist[k]]:
                        #print(smdict[oldlist[k]][i])
                        #input()
                        if newlist[j] in smdict[oldlist[k]][i]:
                            if newpower[j]<smdict[oldlist[k]][i][newlist[j]] + oldpower[k]:
                                newpower[j]=smdict[oldlist[k]][i][newlist[j]] + oldpower[k]
                                newsent[j]=oldsent[k]+newlist[j]
        oldlist=newlist
        oldpower=newpower
        oldsent=newsent

    newpower=0
    newsent='error'
    for k in range(len(oldlist)):
        if newpower < oldpower[k]:
            newpower= oldpower[k]
            newsent=oldsent[k]
    return newsent

if __name__ == "__main__":

    with open('dict2ctotal2','rb') as f:
        smdict=pickle.load(f)

    rvdict,voicedict=loadvoice('../拼音汉字表.txt')

    with open('errorverse','rb') as f:
        pointset= pickle.load(f)
    print('start')

    with open('../input.txt') as f:
        a=f.readline()
        while a!='':
            print(work(a,smdict,rvdict,voicedict,pointset))
            a=f.readline()
