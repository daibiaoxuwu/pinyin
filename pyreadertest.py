#encoding:utf-8
#reader.py 只看含有一个动词的句子(十分之一左右)

import numpy as np
import word2vec
import re
import time
import os
import pickle
import random
import requests
import json
from queue import Queue
#bug:shorten和shorten_front不一样的话,每一遍都得重新计算而不是直接从队列里拿出来!


class reader(object):
    def __init__(self):

#patchlength:每次输入前文额外的句子的数量.
#maxlength:每句话的最大长度.(包括前文额外句子).超过该长度的句子会被丢弃.
#embedding_size:词向量维度数.
        self.maxlength=400

        
        dir0=''
        with open(dir0+'vidict', 'rb') as f:
            self.vidict = pickle.load(f)        #pinyin
        print('v',len(self.vidict))

        self.voicedict={}
        self.rvdict={}
        with open('../拼音汉字表.txt',encoding='gbk') as f:
            a=f.readline()#.encode('gbk')
            while(a!=''):
                b=a.split()
                self.rvdict[b[0]]=b[1:]
                for c in b[1:]:
                    self.voicedict[c]=b[0]
                a=f.readline()

        self.widict={}
        self.maxj=0
        for i in self.rvdict:
            for j in range(len(self.rvdict[i])):
                self.maxj=max(self.maxj,j)
                self.widict[self.rvdict[i][j]]=j
        #        print(self.rvdict[i][j],j)
        print(self.maxj)
        
       # with open(dir0+'widict', 'rb') as f:
       #     self.widict = pickle.load(f)        #汉字
       # print('w',len(self.widict))

        

    def work(self,b1,inputs,pads,answers):
#        for i in a1:
 #               self.vidict[i]=len(self.vidict)
        bb=[self.vidict[i]+2 for i in b1]
        bb.append(1)

        bb=np.array(bb)
#补零
        pads.append(bb.shape[0])
        bb=np.pad(bb,(0,self.maxlength-bb.shape[0]),'constant')
        inputs.append(bb)
        return True

    def list_tags(self,content):
            inputs=[]
            pads=[]
            answers=[]

            b=content.split()#拼音
            while len(b)>self.maxlength-10:
                b1=b[:self.maxlength-10]
                self.work(b1,inputs,pads,answers)
                b=b[self.maxlength-10:]
            self.work(b,inputs,pads,answers)
            return inputs,pads,answers

if __name__ == '__main__':
    model = reader()
    model.list_tags(20000)

