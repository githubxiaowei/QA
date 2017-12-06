import sys,time
import jieba
jieba.load_userdict('dict/dict_unique')

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
    

def processBar(index, totalNum):
    bar = '#'*int((index/totalNum)*50)
    sys.stdout.write(str(int((index/totalNum)*100))+'%  ||'+bar+'->'+str(index)+'/'+str(totalNum)+"\r")
    #sys.stdout.flush()

def is_ch(uchar):
        """判断一个unicode是否是汉字"""
        if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
                return True
        else:
                return False

word2int = {}
idx = 0
with open('dict/dict',encoding='utf8') as fin:
    for line in fin.readlines():
        word = line.split()[0]
        if(word not in word2int):
            word2int[word] = idx
            idx += 1
wordsNum = len(word2int)
print('size of dict: ',len(word2int))



partsNum = 49125


invertedIndex = [BitSet(partsNum) for i in range(wordsNum)]
print('每个字的倒排索引表的字节数：',invertedIndex[0].bytesNum)

for partIdx in range(partsNum):

    processBar(partIdx, partsNum)

    with open('parts/part_'+str(partIdx),encoding='utf8') as f:
        content = f.read()
        for word in jieba.cut_for_search(content):
            try:
                #if(is_ch(word[0])):
                invertedIndex[word2int[word]].insert(partIdx)
            except KeyError as err:
                #print('KEY ERROR'+str(err))
                pass

for idx in range(wordsNum):    
    processBar(idx, wordsNum)
    with open('iidx/ch_'+str(idx)+'.iidx','w',encoding='utf8') as f:
            for j in invertedIndex[idx].set:
                f.write(str(j)+' ')