import sys
import socket
import DSquery
import DSsocket

PORT = 12345
BUF_SIZE = 4096
				
if __name__ == "__main__":
	server = TCPSocket()
	server.bind(('', PORT))
	server.listen(10)
	while True:
		client = server.accept()
		msg = client.sock.recv(BUF_SIZE)
		grep_cmd = msg.decode('utf-8')
		for output in callGrepOnVM(grep_cmd):
			try:
				c.send(output.encode())
			except:
				pass
		c.close()
