import sys
import socket
import DSquery
import DSsocket

PORT = 12345
BUF_SIZE = 4096
<<<<<<< HEAD


def parser_msg(msg):
	msg_d = msg.decode()
	pattern = msg_d.split(' ')[0]
	filename = msg_d.split(' ')[1]
	return pattern, filename


def parser_grep(grepcmd):
	grepcmd_d = grepcmd.decode('utf-8')
	return grepcmd_d
								

=======
				
>>>>>>> 0fae74eba307dd5e638d3b56089d6ec10316097d
if __name__ == "__main__":
	server = TCPSocket()
	server.bind(('', PORT))
	server.listen(10)
	while True:
		client = server.accept()
		msg = client.sock.recv(BUF_SIZE)
		grep_cmd = msg.decode('utf-8')
		for output in callGrepOnVM(grep_cmd):
			try:
				c.send(output.encode())
			except:
				pass
		c.close()
