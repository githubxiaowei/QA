import jieba
from multiprocessing import Pool
import os
import sys
from BitSet import BitSet
from time import time

class searchEngine:
    def __init__(self,partsRange=range(47)): 

        jieba.load_userdict('dict/dict')
        self.word2int = {}
        self.wordsNum = 0
        self.load_dict()
        self.partsRange = partsRange
        #self.pagesNum = 3029940 # 46*256*256+59*256+180 最后一个文件 pages/46/59/180
        self.pages_per_part = 256*256
        self.partsNum = 47 # 分别位于pages/[0-46]
        self.stopWords = ['上','的','什么','什麼','是','大','第几',\
             '过','多少','多少次','？','哪','谁','哪里',\
            '哪个','哪种','哪位','哪座','指','和']
        self.targets = [self.mask(round(self.pages_per_part/8)) for i in range(self.partsNum)] #对每个部分读取倒排索引


    def load_dict(self):
        idx = 0
        with open('dict/dict',encoding='utf8') as fin:
            for line in fin.readlines():
                word = line.split(' ')[0]
                if(word not in self.word2int):
                    self.word2int[word] = idx
                    idx += 1
        self.wordsNum = len(self.word2int)
        #print('size of dict: ',self.wordsNum)

    def readIIDX(self, file):
        with open(file,encoding='utf8') as f:
            s = f.read()[:-1].split(' ')
        bSet = BitSet(len(s)*8)
        for i in range(bSet.bytesNum):
            bSet.set[i] = int(s[i])
        return bSet

    def pageid2fpath(self,partID,id):
        fpath = 'pages/'+str(partID)+'/'+\
                str(id>>8 & 255)+'/'+str(id&255)
        return fpath

    def chid2fpath(self,partID,id): #partID = [0-46]
        fpath = 'iidx/'+str(partID)+'/'+\
                str(id>>16 & 255)+'/'+str(id>>8 & 255)+'/'+str(id&255)+'.iidx'
        return fpath 

    def mask(self,bytes):
        r = BitSet(bytes*8)
        for i in range(bytes):
            r.set[i] = 255
        return r

    

    def findDoc(self,query):

        keyList = []  
        for word in jieba.cut_for_search(query):
            if(word not in self.stopWords):
                try:
                    keyList.append(self.word2int[word])
                except KeyError as e:
                    pass
        #print(keyList)

        for partID in self.partsRange:
            for key in keyList:             
                self.targets[partID].AND(self.readIIDX(self.chid2fpath(partID,key)))

        result = []
        for i in self.partsRange:
            for j in range(self.pages_per_part):
                if(self.targets[i].isElement(j)):
                    result.append(self.pageid2fpath(i,j))  
        #print('doc number: ',len(result))
        return result


if(__name__ == '__main__'):
    beg,end = int(sys.argv[2]),int(sys.argv[3])
    query = sys.argv[1]
    fpath = sys.argv[4]
    result = searchEngine(range(beg,end)).findDoc(query)
    with open(fpath,'w',encoding='utf8') as f:
        for res in result:
            f.write(res+'\n')


