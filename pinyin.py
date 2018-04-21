import pickle
import json
from pypinyin import pinyin, lazy_pinyin, Style


#将句子变为"BOSxxxxxEOS"这种形式
def reform(sentence):
    #如果是以“。”结束的则将“。”删掉
    if sentence.endswith("。"):
        sentence=sentence[:-1]
    #添加起始符BOS和终止符EOS   
    sentence_modify1=sentence.replace("。", "EOSBOS")
    sentence_modify2="BOS"+sentence_modify1+"EOS"
    return sentence_modify2
def listtags(text,smdict,f):
    f.write(text+'\n')
    f.write(' '.join(lazy_pinyin(text,errors='ignore'))+'\n')
    return

if __name__ == "__main__":

    smdict={}
    with open('../pinyin','w') as f:
        for _ in range(1,12):
            text=open('../sina_news/2016-%02d.txt'%_).read()
            for text in open('../sina_news/2016-%02d.txt'%_).readlines():
                listtags(json.loads(text)['html'],smdict,f)
                listtags(json.loads(text)['title'],smdict,f)
            print('one')
