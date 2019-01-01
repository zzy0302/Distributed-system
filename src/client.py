
import sys

import json
import copy
import time
import socket
import DSsocket

SERVER_PORT = 12345
MSGLEN = 4096

def connect_to_server(pattern, filename='./conf.json', unittestmode=0):
	
	with open(filename,'r') as handle:
		nodes = json.loads(handle.read())

	
	for node in nodes:
		node['buffer'] = ''
		node['complete'] = False
		node['count'] = 0
		try:
			node['sock'] = TCPSocket()
			node['sock'].connect((node['ip'], SERVER_PORT))
			patterncopy = copy.deepcopy(pattern)
			patterncopy.append(node['logfile'])
			m = ' '.join(patterncopy)
			node['sock'].send(m)
			node['status'] = True
		except ConnectionRefusedError as e:
			node['status'] = False
			node['complete'] = True


	while True:
		for node in nodes:
			if node['status'] and not node['complete']:
				try:
					if node['sock'].activityDetected(5):
						chunk = node['sock'].recv(MSGLEN)
						if chunk == '':
							node['complete'] = True
							continue
						node['buffer'] += chunk
						records = node['buffer'].split('\n')
						for i in range(len(records) - 1):
							if unittestmode == 0:
								print(node['name'] + ': ' + records[i])
							node['count'] += 1
						node['buffer'] = records[-1]
					else:
						node['complete'] = True
						continue
				except ConnectionRefusedError as e:
					print(str(e) + ': ' + node['name'])
					node['status'] = False
					node['complete'] = True

		if reduce((lambda x,y:x and y), [node['complete'] for node in nodes]):
			for node in nodes:
				if not node['status']:
					print(node['name'] + " encountered an error.")
				else:
					print(node['name'] + " finished with " + str(node['count']) + " lines")
			break
	return nodes
	

if __name__ == "__main__":
	pattern = sys.argv[1:]
	start = time.time()
	connect_to_server(pattern)
	end = time.time()
	print("Query time: %.6fs" %(end - start))

	

