# idf(ch) = log(total DocumentNum / Num of documents containing ch)
import math
import sys

wordsNum = 583280
partsNum = 49125

class BitSet:
    def __init__(self, elementNum):
        self.bytesNum = round(elementNum/8)
        self.set = bytearray(self.bytesNum)
        
    def insert(self, index):
        if(index >= 0 and index>>3 < self.bytesNum):
            self.set[index >> 3] = self.set[index >> 3] | (1 << int(index & 7)) 
            return True;
        return False;
    
    def isElement(self, index):
        if(index >= 0 and index>>3 < self.bytesNum and (self.set[index >> 3] & (1<<(index & 7)))):
            return True
        return False
        
    def AND(self, bs):
        a = BitSet(self.bytesNum*8)
        for i in range(self.bytesNum):
            a.set[i] = self.set[i] & bs.set[i]
        return a

def readIidx(file):
    with open(file,encoding='utf8') as f:
        s = f.read()[:-1].split(' ')
    bSet = BitSet(len(s)*8)
    for i in range(bSet.bytesNum):
        bSet.set[i] = int(s[i])
    return bSet

def processBar(index, totalNum):
    bar = '#'*int((index/totalNum)*50)
    sys.stdout.write(str(int((index/totalNum)*100))+'%  ||'+bar+'->'+str(index)+'/'+str(totalNum)+"\r")

RUN_idf = 1
if(RUN_idf):
    
    idf = [0.0 for i in range(wordsNum)]

    for idx in range(wordsNum):
        processBar(idx, wordsNum)
        num = 0
        iidxFile = 'iidx/ch_'+str(idx)+'.iidx'
        bs = readIidx(iidxFile)
        for i in range(partsNum):
            if(bs.isElement(i)):
                num += 1
        idf[idx] = math.log(partsNum/(num+1)) # divide by zero

    with open('iidx/idf','w',encoding='utf8') as fout:
        for i in idf:
            fout.write(str(i)+' ')
    