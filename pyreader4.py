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
        for i in range(len(a1)):
            if b1[i]=='nve': b1[i]='nue'
            if b1[i]=='lve': b1[i]='lue'
            if b1[i]=='n': b1[i]='en'
            if b1[i]=='bia': b1[i]='bian'
            if b1[i]=='cho': b1[i]='chou'
            if b1[i]=='puo': b1[i]='po'
            if b1[i]=='yie': b1[i]='ye'
            if b1[i] not in self.rvdict:
                print('allnotin',b1[i],a1[i])
                return False
            if a1[i] in self.rvdict[b1[i]]:
                aa.append(self.rvdict[b1[i]].index(a1[i])+2)
            else:
                #print('er',b1[i],a1[i])
                #print('er2',self.rvdict[b1[i]])
            #    print(self.rvdict[b1[i]].index(a1[i]))
                return False


        for i in b1:
            if i not in self.vidict:
                self.vidict[i]=len(self.vidict)
                print(i)
        bb=[self.vidict[i]+2 for i in b1]

#补零
        if(len(aa)!=len(bb)):
            return False
        inputs.append(aa)
        answers.append(bb)
        return True

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
                while len(a)>self.maxlength:
                    a1=a[:self.maxlength]
                    b1=b[:self.maxlength]
                    a=a[self.maxlength:]
                    b=b[self.maxlength:]
                    if self.work(a1,b1,inputs,answers)==False:
                        flag=1
                        break
                    if len(inputs)>=batch_size:
                        return inputs,answers

                if flag==1: continue
                if len(inputs)>=batch_size:
                    return inputs,answers
                if self.work(a,b,inputs,answers)==False:continue
            return inputs,answers

if __name__ == '__main__':
    model = reader()
    model.list_tags(10000000)
    print(len(model.vidict))

