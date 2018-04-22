import pickle
import json
import math


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

def work(line,dict2c,dict3c,rvdict,voicedict):
    line=line.split()
    rightsent=[]
    power=[]

    for i in range(len(line)+1):
        rightsent.append(dict())
        power.append(dict())

#    rightsent[0]=['BOF']

    def req(dic,wd,neww,oldw=None):
        if wd in dic and neww in dic[wd]:
            if oldw==None:return dic[wd][neww]
            elif oldw in dic[wd][neww]:return dic[wd][neww][oldw]
        return 0
        
    def put(i,wd,neww,oldw,value):
        if wd not in power[i]:power[i][wd]={}
        if neww not in power[i][wd]:power[i][wd][neww]=0
            
        if value>power[i][wd][neww]:
            power[i][wd][neww]=value
            if wd not in rightsent[i]:rightsent[i][wd]={}
#            if neww not in rightsent[i-1]:rightsent[i-1][neww]={}
#            if oldw not in rightsent[i-1][neww]:rightsent[i-1][neww][oldw]=''
            try:
                rightsent[i][wd][neww]=rightsent[i-1][neww][oldw]+wd
            except Exception as e:
#                print(i,wd,neww,oldw)
                pass
    if(len(line)==1):
        return('tooshort')

    for neww in rvdict[line[1]]:
        power[1][neww]={}
        rightsent[1][neww]={}
        for oldw in rvdict[line[0]]:
            if neww in dict2c and oldw in dict2c[neww]:
                power[1][neww][oldw]=dict2c[neww][oldw]
            rightsent[1][neww][oldw]=oldw+neww


    for i in range(2,len(line)):
        for wd in rvdict[line[i]]: #遍历所有可能的rvdict
            for neww in rvdict[line[i-1]]:
                for oldw in rvdict[line[i-2]]:
                    put(i,wd,neww,oldw,max(req(dict3c,oldw,neww,wd),req(dict2c,neww,wd))+req(power[i-1],neww,oldw))
                    

    maxwd=-1
    for wd in power[len(line)-1]:
        for neww in power[len(line)-1][wd]:
            if power[len(line)-1][wd][neww]>maxwd:
                maxwd=power[len(line)-1][wd][neww]
                try:
                    ans=rightsent[len(line)-1][wd][neww]
                except:
                    ans='error'
    return ans

if __name__ == "__main__":

    rvdict,voicedict=loadvoice('../拼音汉字表.txt')
    with open('dict2c3','rb') as f:
        dict2c=pickle.load(f)
    with open('dict3c','rb') as f:
        dict3c=pickle.load(f)
    #jiebasm3={'硕士': {'毕': {'ye': {'业': 1}}}, '毕业': {'于': {'': {'': 1}}}, '中国科学院': {'计': {'suan suo': {'算所': 1}}}, '于': {'中': {'guo ke xue yuan': {'国科学院': 1}}}, 'BOF': {'小': {'ming': {'明': 1}}}, '小明': {'硕': {'shi': {'士': 1}}}}
    #jiebasg={'于': 1}
    #小明硕士毕业于中国科学院计算所，后在日本京都大学深造"
    #a='xiao ming shuo shi bi ye yu zhong guo ke xue yuan ji suan suo hou zai ri ben jing du da xue shen zao'
    #print(work(a,dict2c,dict3c,rvdict,voicedict))
    '''
    with open('../input.txt') as f:
        a=f.readline()
        while a!='':
            print(work(a,jiebasm3,jiebasm,jiebasg,rvdict,voicedict))
            a=f.readline()
            '''
    total=0
    right=0
    with open('../output1.txt',encoding='utf-8') as g:
        with open('../input1.txt') as f:
            a=f.readline()
            while a!='':
                ans=work(a,dict2c,dict3c,rvdict,voicedict)
                trueans=g.readline()
                if ans==trueans[:-1]: right+=1
                total+=1
                print(right,total,right/total,ans,trueans[:-1])
                a=f.readline()
