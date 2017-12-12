import socket
import struct, time
import sys
from search import searchEngine


# user-accessible port
PORT = int(sys.argv[1])
beg = int(sys.argv[2])
end = int(sys.argv[3])
se = searchEngine(range(beg,end))
# establish server
service = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
service.bind(("", PORT))
service.listen(1)

print("listening on port", PORT)
buffer_size = 1024

while 1:
	try:
	    # serve forever
	    channel, info = service.accept()
	    print("PORT:{} searching part{}-{}".format(PORT, beg, end))
	    r = channel.recv(buffer_size).decode()
	    length = int(r[:10])
	    recieved = r[10:]
	    for i in range(int((length-1)/buffer_size)):
	    	recieved += channel.recv(buffer_size).decode()
	    print(recieved)

	    result = '|'.join(se.findDoc(recieved))
	    print(result)

	    channel.sendall((str(len(result)+10).zfill(10)+result).encode())

	    #channel.sendall('{}'.format(q).encode()) # send timestamp
	    channel.close() # disconnect
	except Exception as e:
		print(e)

