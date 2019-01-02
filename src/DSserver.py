import re
import sys
import copy
import socket
import subprocess
from DSsocket import *

_port = 20003
_buffer_size = 4096


def call_grep_cmd(command: str) -> bytes:
	try:
		result = subprocess.check_output(command, shell=True)
		result = str(output.decode('utf-8'))
		output_list = list(filter(result.split("\n")))
		for item in output_list:
			yield item + '\n'
	except subprocess.CalledProcessError as error:
		if error.returncode == 1:
			yield


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
			except Exception:
				pass
		client.close()

		
