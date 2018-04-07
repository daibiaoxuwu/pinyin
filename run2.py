import pickle


#将句子变为"BOSxxxxxEOS"这种形式
def reform(sentence):
    #如果是以“。”结束的则将“。”删掉
    if sentence.endswith("。"):
        sentence=sentence[:-1]
    #添加起始符BOS和终止符EOS   
    sentence_modify1=sentence.replace("。", "EOSBOS")
    sentence_modify2="BOS"+sentence_modify1+"EOS"
    return sentence_modify2

if __name__ == "__main__":

    #语料句子
    smdict={}
    for _ in range(1,12):
#        text=reform(open('../sina_news/2016-%02d.txt'%_).read())
        text=open('../sina_news/2016-%02d.txt'%_).read()
        for i in range(0,len(text)-1):
            smtext=text[i:i+2]
            word=text[i]
            if smdict.hasattr(word):
                bigdict=smdict[word]
                if bigdict.hasattr(smtext):
                    bigdict[smtext]+=1
                else:
                    bigdict[smtext]=1
            else:
                smdict[word]={smtext:1}
    print(smdict)

