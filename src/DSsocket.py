import queue
import socket
import select
import telnetlib
import threading

class TCPSocket:
	def __init__(self, sock=None):
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except SocketError as e:
			print(str(e) + ' : ' + self.__class__.__name__)

	def get_ip_status(ip):
	server = telnetlib.Telnet()
	for port in range(20,100):
		try:
			server.open(ip,port)
			print('{0} port {1} is open'.format(ip, port))
			node.join(ip)
		except Exception as err:
			print('{0} port {1} is not open'.format(ip,port))
		finally:
			server.close()

	def check_open(q):
		try:
			while True:
				ip = q.get_nowait()
				get_ip_status(ip)
		except queue.Empty as e:
			pass		

	def scanning:
		try:	
			myname = socket.getfqdn(socket.gethostname())
			myaddr = socket.gethostbyname(myname)
			a = str(myaddr).split(".")
			host = a[0]+'.'+a[1]+'.'+a[2]+'.'
			q=queue.Queue()
			for i in range(20000,20010):
				q.put(host+str(i))
			threads = []
			node = []
			for i in range(10):
				t = threading.Thread(target=check_open,args=(q,))
				t.start()
				threads.append(t)
			for t in threads:
				t.join()
			print(node)
		except SocketError as e:
			print(str(e) + ' : ' + self.__class__.__name__)
	def connect(self, host_port):
		try:
			self.sock.connect(host_port)
		except SocketError as e:
			print(str(e) + ' : ' + self.__class__.__name__)

	def close(self):
		try:
			self.sock.close()
		except SocketError as e:
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
		except SocketError as e:
			print(str(e) + ' : ' + self.__class__.__name__)

	def recv(self, msgLen):
		try:
			chunks = []
			bytes_recd = 0
			while bytes_recd < msgLen:
				chunk = self.sock.recv(msgLen - bytes_recd)
				chunks.append(chunk)
				bytes_recd = bytes_recd + len(chunk)
		except SocketError as e:
			print(str(e) + ' : ' + self.__class__.__name__)
		return b''.join(chunks).decode()

	def bind(self, address_port):
		try:
		   	self.sock.bind(address_port)
		except SocketError as e:
			print(str(e) + ' : ' + self.__class__.__name__)

	def listen(self, backlog):
		try:
			self.sock.listen(backlog)
		except SocketError as e:
			print(str(e) + ' : ' + self.__class__.__name__)

	def accept(self):
		try:
			client_sock, client_info = self.sock.accept()
			return TCPSocket(client_sock), client_info
		except SocketError as e:
			print(str(e) + ' : ' + self.__class__.__name__)
			
	def activityDetected(self, timeout = None):
		if timeout == None:
			ready_to_read, ready_to_write, in_error = select.select([self.sock], [], [])
		else:
			ready_to_read, ready_to_write, in_error = select.select([self.sock], [], [], timeout)
		return len(ready_to_read) > 0