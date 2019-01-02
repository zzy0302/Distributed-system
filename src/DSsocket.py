import os
import json
import queue
import socket
import select
import telnetlib
import threading


file_name = 'config.json'
number = 0
def get_ip_status(ip):
	global file_name
	with open(file_name, 'a') as file_obj:
		global number
		port = 22
		try:
			server = telnetlib.Telnet(ip,port,timeout=3)
			node = {'name': 'node_' + str(number), 'ip': str(ip), 'port': str(port)}
			number = number + 1
			# print (node)
			json.dump(node, file_obj)
			file_obj.write(',')
			# print("node " + str(number) + " has been added.")
		except Exception as err:
			pass
			

def check_open(q):
	try:
		while True:
			ip = q.get_nowait()
			get_ip_status(ip)
	except queue.Empty as e:
		pass		

def DSscanning():
	with open(file_name, 'w') as file_obj:
		file_obj.write('[')
	node = []
	global number 
	number = 0
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 80))
	myaddr = s.getsockname()[0]
	s.close()
	a = str(myaddr).split(".")
	host = a[0]+'.'+a[1]+'.'+a[2]+'.'
	q=queue.Queue()
	for i in range(1,255):
		q.put(host+str(i))
	threads = []
	for i in range(255):
		t = threading.Thread(target=check_open,args=(q,))
		t.start()
		threads.append(t)
	for t in threads:
		t.join()
	with open(file_name, 'rb+') as file_obj:
		file_obj.seek(-1, os.SEEK_END)
		file_obj.truncate()
	with open(file_name, 'a') as file_obj:
		file_obj.write(']')
	with open(file_name) as file_obj:
		nodes = json.load(file_obj)
		# print(nodes)

class TCPSocket:
	def __init__(self, sock=None):
		if sock is None:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.sock = sock

	def connect(self, host_port):
		try:
			self.sock.connect(host_port)
		except socket.error as e:
			print(str(e) + ' : ' + self.__class__.__name__)


	def close(self):
		try:
			self.sock.close()
		except socket.error as e:
			print(str(e) + ' : ' + self.__class__.__name__)


	def send(self, message):
		try:
			msg=message.encode()
			totalsent = 0
			while totalsent < len(msg):
				sent = self.sock.send(msg[totalsent:])
				if sent == 0:
					raise RuntimeError("Connection ERROR")
				totalsent = totalsent + sent
		except socket.error as e:
			print(str(e) + ' : ' + self.__class__.__name__)

	def recv(self, msgLen):
		try:
			chunks = []
			bytes_recd = 0
			while bytes_recd < msgLen:
				chunk = self.sock.recv(msgLen - bytes_recd)
				chunks.append(chunk)
				bytes_recd = bytes_recd + len(chunk)
		except socket.error as e:
			print(str(e) + ' : ' + self.__class__.__name__)
		return b''.join(chunks).decode()

	def bind(self, address_port):
		try:
		   	self.sock.bind(address_port)
		except socket.error as e:
			print(str(e) + ' : ' + self.__class__.__name__)

	def listen(self, backlog):
		try:
			self.sock.listen(backlog)
		except socket.error as e:
			print(str(e) + ' : ' + self.__class__.__name__)

	def accept(self):
		try:
			client_sock, client_info = self.sock.accept()
			return TCPSocket(client_sock), client_info
		except socket.error as e:
			print(str(e) + ' : ' + self.__class__.__name__)

	def activityDetected(self, timeout = None):
		if timeout == None:
			ready_to_read, ready_to_write, in_error = select.select([self.sock], [], [])
		else:
			ready_to_read, ready_to_write, in_error = select.select([self.sock], [], [], timeout)
		return len(ready_to_read) > 0
