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
        for i in range(self.bytesNum):
            self.set[i] &= bs.set[i]
        return self
        
        '''
        a = BitSet(self.bytesNum*8)
        for i in range(self.bytesNum):
            a.set[i] = self.set[i] & bs.set[i]
        return a
        '''