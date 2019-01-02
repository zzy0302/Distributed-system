import os
import re
import sys
import copy
import time
import socket
import threading
import subprocess
from DSsocket import *

_flag = 0
_port = 20009
_buffer_size = 4096
file_name = 'config.json'

def call_grep_cmd(command: str) -> bytes:
	try:
		result = subprocess.check_output(command, shell=True)
		result = str(result.decode('utf-8'))
		output_list = list(filter(None, result.split("\n")))
		for item in output_list:
			yield item + '\n'
	except subprocess.CalledProcessError as error:
		if error.returncode == 1:
			yield

def _scan():
	global _flag
	while True and _flag:
		DSscanning()
		os.remove(file_name)
		os.rename('temp.json', file_name)
		time.sleep(2)
	print (_flag)
		



if __name__ == "__main__":
	server = TCPSocket()
	server.bind(('', _port))
	server.listen(10)
	scan=threading.Thread(target=_scan)
	scan.start()
	while True:
		_flag = 1
		_flag = 0
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
		
