import sys
import socket
import DSquery
import DSsocket
PORT = 12345
BUF_SIZE = 4096

def parser_msg(msg):
	msg_d = msg.decode()
	pattern = msg_d.split(' ')[0]
	filename = msg_d.split(' ')[1]
	return pattern, filename


def parser_grep(grepcmd):
	grepcmd_d = grepcmd.decode('utf-8')
	return grepcmd_d
								

if __name__ == "__main__":
	s = TCPSocket()
	s.bind(('', PORT))
	s.listen(10)

	while True:
		c, addr = s.accept()
		msg = c.sock.recv(BUF_SIZE)
		grep_cmd = parser_grep(msg)
		# do query
		print(grep_cmd)
		#query_result = doQuery(pattern, filename)
		for output in callGrepOnVM(grep_cmd):
			try:
				c.send(output.encode())
			except:
				continue
		c.close()
