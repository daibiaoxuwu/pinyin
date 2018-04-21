import pickle
import json
#import sys
#reload(sys)
#sys.setdefaultencoding('gbk')


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

def total(smdict):
    voicedict={}
    with open('../拼音汉字表.txt',encoding='gbk') as f:
        a=f.readline()#.encode('gbk')
        while(a!=''):
            b=a.split()
            for c in b[1:]:
                voicedict[c]=b[0]
            a=f.readline()
    print('loadedvoice')

    newdict={}
    pointset=set()
    for i in smdict:
  #      print('i',type(i),i)
 #       input()
        tempdict={}
        totalsum={}
        for j in smdict[i]:
#            print('j',type(j),j,smdict[i][j],j[0],j[1])
            if j[1] not in voicedict:#标点符号
                if j[1] not in pointset:
                    print('errorverse',j[1])
                    pointset.add(j[1])
            else:
                voice=voicedict[j[1]] 
                if voice in tempdict:#已经加入了二级dict,放入三级dict
                    tempdict[voice][j[1]]=smdict[i][j]
                    totalsum[voice]+=smdict[i][j]
                else:
                    tempdict[voice]={j[1]:smdict[i][j]}
                    totalsum[voice]=smdict[i][j]
        #除法,'安quan':'全'+'权'+'...'的和是1
        for voice in tempdict:
            for word in tempdict[voice]:
                tempdict[voice][word]/=totalsum[voice]

        newdict[i]=tempdict
    with open('errorverse','wb') as f:
        pickle.dump(pointset,f)
    return newdict



if __name__ == "__main__":
    with open('dict2c','rb') as f:
        smdict=pickle.load(f)
    #print(smdict)
    print('loadedsmdict')

    with open('dict2ctotal','wb') as f:
        pickle.dump(total(smdict),f)
        #print(total(smdict))

