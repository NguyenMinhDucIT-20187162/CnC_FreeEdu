#!/usr/bin/python3

import socket
from termcolor import colored

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

