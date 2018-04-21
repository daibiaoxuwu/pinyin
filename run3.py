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

def work(line,jiebasm,jiebasg,rvdict,voicedict):

    line=line.split()

    rightsent=['']*(len(line)+1)

    power=[0]*(len(line)+1)
    power[0]=0

    for en in range(0,len(line)):#i 拼音

        maxwd=-1
        for wd in jiebasg:
            if wd in voicedict and voicedict[wd]==line[en] and jiebasg[wd]>maxwd:
                maxwd=jiebasg[wd]
                rightwd=wd
        if maxwd>=0:
            rightsent[en+1]=rightsent[en]+rightwd #第0个字出来的时候存到rightsent[1] rightsent[0]永远为0
            power[en+1]=maxwd#一个词的power? power[0]:永远为0.第0个字出来的时候写道power[1]
            print(en,rightsent[en+1])


        for st in range(1,en+1):  #再看多字的词 从1到en
            for firstwd in rvdict[line[st-1]]:   #未知区第一个字是什么(从0到en-1)
                if firstwd not in jiebasm: continue  
                voice=(' '.join(line[st:en+1])+' ')
                if voice  in jiebasm[firstwd]: #这个词出现过
                    tpdict=jiebasm[firstwd][voice]
                    maxwd=-1
                    for wds in tpdict:
                        if tpdict[wds]>maxwd:
                            maxwd=tpdict[wds]
                            rightwds=wds
                    newpow=power[st-1]+maxwd*pow(en-st+2,2)
                    if power[en+1]<newpow:
                        rightsent[en+1]=rightsent[st-1]+firstwd+rightwds#找到念这个的最好的词
                        print(en,rightsent[en+1],st,rightsent[st-1])
                        power[en+1]=newpow
    return rightsent[len(line)]

if __name__ == "__main__":

#    with open('dict2clog','rb') as f:
    '''
    with open('../jiebasm','rb') as f:
        jiebasm=pickle.load(f)
    with open('../jiebasg','rb') as f:
        jiebasg=pickle.load(f)
    '''
    jiebasm={'硕': {'shi ': {'士': 1}}, '小': {'ming ': {'明': 1}}, '毕': {'ye ': {'业': 1}}, '科': {'xue yuan ': {'学院': 1}, 'xue ': {'学': 1}}, '学': {'yuan ': {'院': 1}}, '大': {'xue ': {'学': 1}}, '深': {'zao ': {'造': 1}}, '京': {'du ': {'都': 1}}, '日': {'ben ': {'本': 1}, 'ben jing du dai xue ': {'本京都大学': 1}}, '中': {'guo ke xue yuan ': {'国科学院': 1}, 'guo ': {'国': 1}}, '计': {'suan suo ': {'算所': 1}, 'suan ': {'算': 1}}}
    jiebasg={'于': 1, '在': 1, '，': 1, '后': 1}
    jiebasg={'于': 1, '在': 1, '，': 1, '后': 1, '晓': 4}

    rvdict,voicedict=loadvoice('../拼音汉字表.txt')

    #小明硕士毕业于中国科学院计算所，后在日本京都大学深造"
    a='xiao ming shuo shi bi ye yu zhong guo ke xue yuan ji suan suo hou zai ri ben jing du da xue shen zao'
    print(work(a,jiebasm,jiebasg,rvdict,voicedict))
    '''
    with open('../input.txt') as f:
        a=f.readline()
        while a!='':
            print(work(a,jiebasm,jiebasg,rvdict,voicedict))
            a=f.readline()
    '''
