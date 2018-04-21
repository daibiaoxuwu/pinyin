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
    def __init__(self, maxlength=400):

#patchlength:每次输入前文额外的句子的数量.
#maxlength:每句话的最大长度.(包括前文额外句子).超过该长度的句子会被丢弃.
#embedding_size:词向量维度数.
        self.maxlength=maxlength

        
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

        self.resp=open('../pinyin').readlines()
        self.readlength=len(self.resp)
        self.pointer=0
        


    def list_tags(self,batch_size):
        while True:#防止读到末尾
            inputs=[]
            pads=[]
            answers=[]
            while len(inputs)<batch_size:
                if self.pointer==self.readlength:
                    self.pointer=0
                    return None,None,None,None,None,None
                a0=self.resp[self.pointer]#汉字
                a=''
                for i in a0:
                    if i in self.widict:
                        a+=i
                if len(a)<5:
                    print('tooshort',a)
                    self.pointer+=1
                    continue
                b=self.resp[self.pointer+1].split()#拼音
                self.pointer+=2
                a1=a
                b1=b
                while len(a)>self.maxlength-10:
                    a1=a[:self.maxlength-10]
                    b1=b[:self.maxlength-10]
                    a=a[self.maxlength-10:]
                    b=b[self.maxlength-10:]
                aa=[self.widict[i]+2 for i in a1]
                aa.append(1)
                try:
                    bb=[self.vidict[i]+2 for i in b1]
                except:
                    print('bb key error',b1)
                    self.pointer+=1
                    continue
                bb.append(1)
                aa=np.array(aa)
                bb=np.array(bb)
#补零
                print(aa.shape[0],bb.shape[0],a0)
                pads.append(aa.shape[0])
                aa=np.pad(aa,(0,self.maxlength-aa.shape[0]),'constant')
                bb=np.pad(bb,(0,self.maxlength-bb.shape[0]),'constant')
                inputs.append(aa)
                answers.append(bb)
            return inputs,pads,answers

if __name__ == '__main__':
    model = reader()
    model.list_tags(200)

