import sys
import json
import copy
import time
import socket
import DSsocket
from DSsocket import *

_server_port = 12345
_message_length = 4096


def node_process(nodes: dict) -> dict:
	global _server_port

	params = {'buf': '', 'complete': False, 'count': 0}
	for node in nodes:
		node.update(params)

		try:
			node['sock'] = TCPSocket()
			node['sock'].connect((node['ip'], _server_port))
			pattern_copy = copy.deepcopy(pattern)
			pattern_copy.append(node['log_path'])
			m = ' '.join(pattern_copy)
			node['sock'].send(m)
			node['status'] = True
		except ConnectionRefusedError as e:
			node['status'] = False
			node['complete'] = True

	return nodes


def node_detected(node: dict, mode: int) -> dict:
	global _message_length

	if node['status'] and not node['complete']:
		try:
			if node['sock'].activityDetected(5):
				chunk = node['sock'].recv(_message_length)
				if chunk == '':
					node['complete'] = True
					return node
				node['buffer'] += chunk
				records = node['buffer'].split('\n')
				for i in range(len(records) - 1):
					if mode == 0:
						print(node['name'] + ': ' + records[i])
					node['count'] += 1
				node['buffer'] = records[-1]
			else:
				node['complete'] = True
				return node
		except ConnectionRefusedError as e:
			print(str(e) + ': ' + node['name'])
			node['status'] = False
			node['complete'] = True
			return node


def connect_to_server(pattern, filename='config.json', mode=0):
	with open(filename,'r') as file_obj:
		nodes = json.loads(file_obj.read())
	
	nodes = node_process(nodes)

	while True:
		for node in nodes:
			node = node_detected(node)

		if reduce((lambda x,y: x and y), [node['complete'] for node in nodes]):
			for node in nodes:
				if not node['status']:
					print(node['name'] + 'caught an error.')
				else:
					print(node['name'] + " completed with " + str(node['count']) + ' lines.')
			break

	return nodes


if __name__ == "__main__":
	pattern = sys.argv[1:]
	start = time.time()
	connect_to_server(pattern)
	end = time.time()
	print("Query time: %.4fs" %(end - start))
