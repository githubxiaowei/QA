from multiprocessing import Pool
import os
from time import time


def sub_process(id,partsRange,query):
    cmd = 'python search.py '+\
            query+' '+\
            str(partsRange[0])+' '+\
            str(partsRange[1])+' '+\
            result_path(id)
    os.system(cmd)

def result_path(id):
    result_dir = 'result/'
    if(not os.path.exists(result_dir)):
        os.mkdir(result_dir)
    return result_dir+str(id)

def divide(totalParts, processorNum):
    part_per_process = int((totalParts+processorNum-1)/processorNum)
    return [[i*part_per_process,min(totalParts,(1+i)*part_per_process)] for i in range(processorNum)]

if __name__=='__main__':

    query = '中华人民共和国共产党的领导人是谁'

    start = time()

    totalParts = 47
    processorNum = 6
    ranges = divide(totalParts, processorNum)
    print(ranges)

    p = Pool(processorNum)
    for id,partsRange in enumerate(ranges):
        p.apply_async(sub_process, args=(id,partsRange,query))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')

    result = []
    for id in range(processorNum):
        with open(result_path(id),encoding='utf8') as f:
            for line in f.readlines():
                result.append(line.strip('\n'))
    print(result)
    print('用时 {} s'.format(time()-start))
