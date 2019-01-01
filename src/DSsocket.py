import socket
import select
class TCPSocket:
	def __init__(self, sock=None):
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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