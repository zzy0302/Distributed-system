import queue
import socket
import select
import telnetlib
import threading

def get_ip_status(ip):
	server = telnetlib.Telnet()
	port = 22
	try:
		server.open(ip,port)
		print('{0} port {1} is open'.format(ip, port))

	except Exceptio n as err:
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

if __name__ == "__main__":
	try:	
		myname = socket.getfqdn(socket.gethostname())
		myaddr = socket.gethostbyname(myname)
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
	except SocketError as e:
		print(str(e) + ' : ' + self.__class__.__name__)
