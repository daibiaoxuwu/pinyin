#encoding:utf-8
#reader.py 只看含有一个动词的句子(十分之一左右)
import pickle


if __name__ == '__main__':
    vdict={}
    wdict={}
    f=open('../pinyin2')
    while True:
        a=f.readline()
        if a=='':
            break
        for i in a:
            if i not in vdict:
                if i=='nve': i='nue'
                if i=='lve': i='lue'
                if i=='n': i='en'
                if i=='bia': i='bian'
                if i=='cho': i='chou'
                if i=='puo': i='po'
                if i=='yie': i='ye'
                vdict[i]=len(vdict)

        a=f.readline()
        for i in a.split():
            if i not in wdict:
                wdict[i]=len(wdict)

    with open('vidict','wb') as f:
        pickle.dump(vdict,f)
    with open('widict','wb') as f:
        pickle.dump(wdict,f)
