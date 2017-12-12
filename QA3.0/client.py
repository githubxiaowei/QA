import socket
import os
from multiprocessing import Pool
import struct, sys, time


buffer_size = 1024


def query(host, port, q):
	# fetch time buffer from stream server
	print('connecting '+str(port))
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((host, port))
	s.sendall((str(len(q)+10).zfill(10)+q).encode())
	r = s.recv(buffer_size).decode()
	length = int(r[:10])

	recieved = r[10:]
	for i in range(int((length-1)/buffer_size)):
		recieved += s.recv(buffer_size).decode()

	s.close()
	return recieved



if __name__ == "__main__":
	# default server
	host = "localhost"
	while(1):
		try:
			q = input('search:\n')
			result = []
			p = Pool(10)
			for id in range(10):
				result.append(p.apply_async(query, args=(host,7777+id,q)))
			#print('Waiting for all subprocesses done...')
			p.close()
			p.join()
			#result = '|'.join([res.get() for res in result])
			for res in result:
				print(res.get())
		except Exception as e:
			print(e)






