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

    rightsent=[{}]*(len(line)+1)
#    rightsent[0]=['BOF']

    power=[{}]*(len(line)+1)

    for wd in jiebasg:
        if wd in voicedict and voicedict[wd]==line[0]:
            rightsent[0][wd]=jiebasg[wd]        #初始 单个字权重
    for wd in jiebasm:
        if wd in voicedict and voicedict[wd]==line[0]:
            for i in jiebasm[wd]:
                if i==line[:len(i)]:
                    for j in jiebasm[wd][i]:#同音字
                        rightsent[len(i)][wd+j]=wd+j
                        power[len(i)][wd+j]=jiebasm[wd][i][j]*pow(len(i)+1,2) #单个词bonus


    for en in range(1,len(line)):#i 拼音
        for wd in jiebasg:
            if wd in voicedict and voicedict[wd]==line[en]:
                for enen in range(0,en):
                    for odwd in power[enen]:
                        if len(odwd)==en-enen: #odwd符合要求
                            if odwd in jiebasm3 and wd in jiebasm3[odwd][wd]:
                                score=power[en-1][odwd] + jiebasm3[odwd][wd]['']['']*power(2,3) + jiebasg[wd]  #跨词权重
                            else:
                                score=power[en-1][odwd] + jiebasg[wd]
                            if wd not in power[en] or (wd in power[en] and power[en][wd]<score):
                                power[en][wd]=score
                                rightsent[en][wd]=rightsent[en-1][odwd]+wd

        for wd in jiebasm:
            if wd in voicedict and voicedict[wd]==line[en]:
                for i in jiebasm[wd]:
                    if i==line[:len(i)]:
                        for j in jiebasm[wd][i]:#同音字
                            for enen in range(0,en):
                                for odwd in power[enen]:
                                    if len(odwd)==en-enen: #odwd符合要求
                                        if odwd in jiebasm3 and wd in jiebasm3[odwd][wd]:
                                            score=power[en-1][odwd] + jiebasm3[odwd][wd][i][j]*power(len(i)+1,3) + jiebasm[wd][i][j]*power(len(i)+1,2)  #跨词权重
                                        else:
                                            score=power[en-1][odwd] + jiebasm[wd][i][j]*power(len(i)+1,2)
                                        if wd+j not in power[en] or (wd+j in power[en] and power[en][wd+j]<score):
                                            power[en][wd+j]=score
                                            rightsent[en][wd]=rightsent[enen][odwd]+wd+j
    maxwd=-1
    for i in power[len(line)-1]:
        if power[len(line)-1][i]>maxwd:
            maxwd=power[len(line)-1][i]
            ans=rightsent[len(line)-1][i]
    return ans

if __name__ == "__main__":

    rvdict,voicedict=loadvoice('../拼音汉字表.txt')
#    with open('dict2clog','rb') as f:
    with open('../jiebasm3','rb') as f:
        jiebasm3=pickle.load(f)
    with open('jiebasm','rb') as f:
        jiebasm=pickle.load(f)
    with open('jiebasg','rb') as f:
        jiebasg=pickle.load(f)
    jiebasm3={'硕士': {'毕': {'ye': {'业': 1}}}, '毕业': {'于': {'': {'': 1}}}, '中国科学院': {'计': {'suan suo': {'算所': 1}}}, '于': {'中': {'guo ke xue yuan': {'国科学院': 1}}}, 'BOF': {'小': {'ming': {'明': 1}}}, '小明': {'硕': {'shi': {'士': 1}}}}
    jiebasg={'于': 1}
    #小明硕士毕业于中国科学院计算所，后在日本京都大学深造"
    a='xiao ming shuo shi bi ye yu zhong guo ke xue yuan ji suan suo hou zai ri ben jing du da xue shen zao'
    print(work(a,jiebasm3,jiebasm,jiebasg,rvdict,voicedict))
    '''
    with open('../input.txt') as f:
        a=f.readline()
        while a!='':
            print(work(a,jiebasm,jiebasg,rvdict,voicedict))
            a=f.readline()
    '''
