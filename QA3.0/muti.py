from multiprocessing import Pool
import os

def server(id,partsRange):
	cmd = 'python server.py '+\
	str(7777+id)+' '+\
	str(partsRange[0])+' '+\
	str(partsRange[1])

	os.system(cmd)


def divide(totalParts, processorNum):
    part_per_process = int((totalParts+processorNum-1)/processorNum)
    return [[i*part_per_process,min(totalParts,(1+i)*part_per_process)] for i in range(processorNum)]

if(__name__ == '__main__'):

	totalParts = 47
	processorNum = 10
	ranges = divide(totalParts, processorNum)

	p = Pool(processorNum)
	for id,partsRange in enumerate(ranges):
	    p.apply_async(server, args=(id,partsRange))
	#print('Waiting for all subprocesses done...')
	p.close()
	p.join()

	
