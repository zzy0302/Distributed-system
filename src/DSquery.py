import re
import sys
import copy
import subprocess



def callGrepOnVM(grepCall):
	pattern = grepCall.split(" ")
	pattern.insert(0,u'grep')
	pattern.insert(1,u'-n')

	try:
		output = subprocess.check_output(pattern).decode('utf-8').strip()
		output = str(output)
		output = output.split("\n")
		for i in range(0, len(output)):
			yield output[i] + '\n'
	except subprocess.CalledProcessError as e:
		if e.returncode  == 1:
			yield
		elif e.returncode == 2:
			yield


if __name__ == '__main__':
	grepCall = sys.argv[1:]
	print(grepCall)
	for output in callGrepOnVM(grepCall):
		print(output)
	
