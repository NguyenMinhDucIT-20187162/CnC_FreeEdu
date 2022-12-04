#!/usr/bin/python3

import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(("192.168.235.132", 1234))

s.close()
