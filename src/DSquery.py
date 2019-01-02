import re
import sys
import subprocess
import copy


def doQuery(pattern, filename):
    pattern2 = pattern
    if pattern2[0:2] != '.*':
        pattern2 = '.*' + pattern2
    if pattern2[-2:] != '.*':
        pattern2 = pattern2 + '.*'
    try:
        re_obj = re.compile(pattern2)
    except:
        print("Invalid query pattern: %s" %pattern)
        return
    f = open(filename, 'r')
    result = []
    for idx, line in enumerate(f.readlines()):
        line = line.strip()
        m = re_obj.match(line)
        if m:
            output = str(idx) + ': ' + line
            result.append(output)
    f.close()
    return '\n'.join(result)


def doQuery2(pattern, filename):
    pattern2 = pattern
    if pattern2[0:2] != '.*':
        pattern2 = '.*' + pattern2
    if pattern2[-2:] != '.*':
        pattern2 = pattern2 + '.*'
    try:
        re_obj = re.compile(pattern2)
    except:
        print("Invalid query pattern: %s" %pattern)
        return
    f = open(filename, 'r')
    for idx, line in enumerate(f.readlines()):
        line = line.strip()
        m = re_obj.match(line)
        if m:
            output = str(idx) + ': ' + line + '\n'
            yield output
    f.close()


def callGrepOnVM(grepCall):
	pattern = grepCall.split(" ")
	pattern.insert(0,u'grep')
	pattern.insert(1,u'-n')

	try:
		output = subprocess.check_output(pattern).decode('utf-8').strip()
		output = str(output)
		output = output.split("\n")
		# print(output)
		# print(len(output))
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
