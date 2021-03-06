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
			print (node)
			json.dump(node, file_obj)
			file_obj.write(',')
			print("node " + str(number) + " has been added.")
		except Exception as err:
			
			print('{0} port {1} is not open'.format(ip,port))

def check_open(q):
	try:
		while True:
			ip = q.get_nowait()
			get_ip_status(ip)
	except queue.Empty as e:
		pass		

if __name__ == "__main__":
	with open(file_name, 'w') as file_obj:
		file_obj.write('[')
	node = []
	number = 0
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
	with open(file_name, 'rb+') as file_obj:
		file_obj.seek(-1, os.SEEK_END)
		file_obj.truncate()
	with open(file_name, 'a') as file_obj:
		file_obj.write(']')
	with open(file_name) as file_obj:
		nodes = json.load(file_obj)
		print(nodes)
