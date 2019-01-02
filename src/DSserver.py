import re
import sys
import copy
import socket
import subprocess
<<<<<<< HEAD

_port = 12345
_buffer_size = 4096


def call_grep_cmd(command: str) -> bytes:
=======
from DSsocket import *

PORT = 20002
BUF_SIZE = 4096

def callGrepOnVM(grepCall):
	pattern = grepCall.split(" ")
	pattern.insert(0,u'grep')
	pattern.insert(1,u'-n')
>>>>>>> daab7a5faa485d62f5cd6c7012504ddcb1c14756
	try:
		result = subprocess.check_output(command, shell=True)
		result = str(output.decode('utf-8'))
		output_list = list(filter(result.split("\n")))
		for item in output_list:
			yield item + '\n'
	except subprocess.CalledProcessError as error:
		if error.returncode == 1:


if __name__ == "__main__":
	DSscanning()
	server = TCPSocket()
	server.bind(('', _port))
	server.listen(10)

	while True:
		client, client_info = server.accept()
		message = client.sock.recv(_buffer_size)
		grep_cmd = message.decode('utf-8')
		for output in call_grep_cmd(grep_cmd):
			try:
				print(output)
				client.send(output.encode())
			except:
				pass
<<<<<<< HEAD
		client.close()
=======
		c.close()
		
>>>>>>> daab7a5faa485d62f5cd6c7012504ddcb1c14756
