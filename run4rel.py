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

def work(line,jiebasm3,jiebasm,jiebasg,rvdict,voicedict):
    jiebasg2=dict()
    for i in jiebasg:
        try:
            jiebasg2[i]=math.log(jiebasg[i]+0.1)-1
        except Exception as e:
            print(jiebasg[i])
            raise e
    jiebasg=jiebasg2
    jiebasm2=dict()
    def putdict(dic,wd,p):
        if wd not in dic:
            dic[wd]=p
        return

        
    for i in jiebasm:
        for j in jiebasm[i]:
            for r in jiebasm[i][j]:
                putdict(jiebasm2,i,{})
                putdict(jiebasm2[i],j,{})
                putdict(jiebasm2[i][j],r,math.log(jiebasm[i][j][r]+0.1))
    jiebasm=jiebasm2

    def valuewd(wd,i,j):#wd 第一个字 i 拼音 j 后面的所有字
        value= jiebasm[wd][i][j]#*pow(len(i.split())+1,2)
        for t in j:
            if t in jiebasg:
                value+=jiebasg[t] 
        if wd in jiebasg:
            value +=jiebasg[wd] #单个词bonus
        return value
        

    def valuewd2(odwd, wd,i,j):#odwd 先导 wd 第一个字 i 拼音 j 后面的所有字
        score= jiebasm3[odwd][wd][i][j]*pow(len(i.split())+1,2)
        if len(wd)==1:
            return score+jiebasg[wd] 
        else:
            return score+valuewd(wd,i,j)
    line=line.split()

    rightsent=[]
    power=[]
    for i in range(len(line)+1):
        rightsent.append(dict())
        power.append(dict())
#    rightsent[0]=['BOF']


    for wd in jiebasg:
        if wd in voicedict and voicedict[wd]==line[0]:
            rightsent[0][wd]=wd        #初始 单个字权重
            power[0][wd]=jiebasg[wd]        #初始 单个字权重

    for wd in jiebasm:
        if wd in voicedict and voicedict[wd]==line[0]:
#            if wd=='小':
            for i in jiebasm[wd]:
                if i.split()==line[1:1+len(i.split())]:
                    for j in jiebasm[wd][i]:                            #同音字
                        rightsent[len(i.split())][wd+j]=wd+j
                        power[len(i.split())][wd+j]=valuewd(wd,i,j)
#                else:


    for en in range(1,len(line)):#i 拼音
        for wd in jiebasg:
            if wd in voicedict and voicedict[wd]==line[en]:
                    for odwd in power[en-1]:
                            if odwd in jiebasm3 and wd in jiebasm3[odwd] and '' in jiebasm3[odwd][wd]:
                                score=power[en-1][odwd] + jiebasm3[odwd][wd][''][''] + jiebasg[wd]  #跨词权重
                            else:
                                score=power[en-1][odwd] + jiebasg[wd]
                            if wd not in power[en] or (wd in power[en] and power[en][wd]<score):
                                power[en][wd]=score
#                                print(en,wd,enen,odwd,power[enen][odwd])
                                rightsent[en][wd]=rightsent[en-1][odwd]+wd

        for wd in jiebasm:
            for stst in range(1,en-1):
                if wd in voicedict and voicedict[wd]==line[stst+1]:
                    for i in jiebasm[wd]:
                        if len(i.split())==en-1-stst and i.split()==line[stst+2:en+1]:
                            for j in jiebasm[wd][i]:#同音字
                                    for odwd in power[stst]:
                                            if odwd in jiebasm3 and wd in jiebasm3[odwd] and i in jiebasm3[odwd][wd]:
                                                score=power[stst][odwd] + valuewd2(odwd,wd,i,j)
                                            else:
                                                score=power[stst][odwd] + valuewd(wd,i,j)

                                               # input()
                                            if wd+j not in power[en] or (wd+j in power[en] and power[en][wd+j]<score):
                                                power[en][wd+j]=score
                                                rightsent[en][wd+j]=rightsent[stst][odwd]+wd+j
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
    with open('../jiebasm','rb') as f:
        jiebasm=pickle.load(f)
    with open('../jiebasg','rb') as f:
        jiebasg=pickle.load(f)
    #jiebasm3={'硕士': {'毕': {'ye': {'业': 1}}}, '毕业': {'于': {'': {'': 1}}}, '中国科学院': {'计': {'suan suo': {'算所': 1}}}, '于': {'中': {'guo ke xue yuan': {'国科学院': 1}}}, 'BOF': {'小': {'ming': {'明': 1}}}, '小明': {'硕': {'shi': {'士': 1}}}}
    #jiebasg={'于': 1}
    #小明硕士毕业于中国科学院计算所，后在日本京都大学深造"
    '''
    a='xiao ming shuo shi bi ye yu zhong guo ke xue yuan ji suan suo hou zai ri ben jing du da xue shen zao'
    print(work(a,jiebasm3,jiebasm,jiebasg,rvdict,voicedict))
    '''
    with open('../input.txt') as f:
        with open('../output.txt','w') as g:
            a=f.readline()
            while a!='':
                ans=work(a,jiebasm3,jiebasm,jiebasg,rvdict,voicedict)
                print(ans)
                g.write(ans)
                a=f.readline()
