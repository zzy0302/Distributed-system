import re
import sys
import copy
import socket
import DSquery
import DSsocket
import subprocess
PORT = 12345
BUF_SIZE = 4096

def callGrepOnVM(grepCall):
	pattern = grepCall.split(" ")
	pattern.insert(0,u'grep')
	pattern.insert(1,u'-n')

	try:
		output = subprocess.check_output(pattern).decode('utf-8').strip()
		output = str(output)
		output = output.split("\n")
		for i in range(0, len(output)):
			yield output[i] + '\n'
	except subprocess.CalledProcessError as e:
		if e.returncode  == 1:
			yield
		elif e.returncode == 2:
			yield

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
