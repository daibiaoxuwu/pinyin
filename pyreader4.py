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
    def __init__(self, maxlength=10):

#patchlength:每次输入前文额外的句子的数量.
#maxlength:每句话的最大长度.(包括前文额外句子).超过该长度的句子会被丢弃.
#embedding_size:词向量维度数.
        self.maxlength=maxlength

        
        dir0=''
        self.vidict = {}

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
        print(self.maxj)
        
       # with open(dir0+'widict', 'rb') as f:
       #     self.widict = pickle.load(f)        #汉字
       # print('w',len(self.widict))

        self.resp=open('../pinyin2').readlines()
        self.readlength=len(self.resp)
        self.pointer=0
        

    def work(self,a1,b1,inputs,answers):
        aa=[]
        bb=[]
        ra=''
        rb=''
        for i in range(self.maxlength):
            if len(b1)==0 or len(a1)==0:break
            if b1[0]=='nve': b1[0]='nue'
            if b1[0]=='lve': b1[0]='lue'
            if b1[0]=='n': b1[0]='en'
            if b1[0]=='bia': b1[0]='bian'
            if b1[0]=='cho': b1[0]='chou'
            if b1[0]=='puo': b1[0]='po'
            if b1[0]=='yie': b1[0]='ye'
            if b1[0] not in self.rvdict:
                print('allnotin',b1[0],a1[0])
                a1=a1[1:]
                b1=b1[1:]
                print(ra,rb)
                inputs.append(aa)
                answers.append(bb)
                return a1,b1
            if a1[0] in self.rvdict[b1[0]]:
                aa.append(self.rvdict[b1[0]].index(a1[0])+2)
                ra+=a1[0]
            else:
                print('er',b1[0],a1[0])
                print('er2',self.rvdict[b1[0]])
                if a1[0] in self.rvdict[b1[1]]:
                    aa.append(self.rvdict[b1[1]].index(a1[0])+2)
                    ra+=a1[0]
                    b1=b1[1:]
                else:
                    inputs.append(aa)
                    answers.append(bb)
                    print('er3',b1[1],a1[0])
                    print('er4',self.rvdict[b1[1]])
                    a1=a1[1:]
                    b1=b1[1:]
                    inputs.append(aa)
                    answers.append(bb)
                    print(ra,rb)
                    return a1,b1
            if b1[0] not in self.vidict:
                self.vidict[b1[0]]=len(self.vidict)
                print(b1[0])
            rb+=b1[0]
            rb+=' '
            bb.append(self.vidict[b1[0]]+2)
            a1=a1[1:]
            b1=b1[1:]


        print(ra,rb)
        inputs.append(aa)
        answers.append(bb)
        return a1,b1

    def list_tags(self,batch_size):
        while True:#防止读到末尾
            inputs=[]
            answers=[]
            while len(inputs)<batch_size:
                if self.pointer==self.readlength:
                    self.pointer=0
                    return None,None
                a0=self.resp[self.pointer]#汉字
                a=''
                for i in a0:
                    if i in self.widict:
                        a+=i
                '''
                if len(a)<5:
                    print('tooshort',a)
                    self.pointer+=1
                    continue
                '''
                b=self.resp[self.pointer+1].split()#拼音
                self.pointer+=2
                flag=0
                while len(a)>0:
                    a,b=self.work(a,b,inputs,answers)
                    if len(inputs)>=batch_size:
                        return inputs,answers

            return inputs,answers

if __name__ == '__main__':
    model = reader()
    model.list_tags(10000000)
    print(len(model.vidict))

