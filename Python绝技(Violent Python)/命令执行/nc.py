#!/usr/bin/python3.6
# -*- coding=utf-8 -*-

import sys
import socket
import getopt
import threading
import subprocess

listen                  =     False
command                 =     False
upload                  =     False
execute                 =     ""
target                  =     ""
upload_destination      =     ""
port                    =     0

def usage():
    pinrt ('owen net tool')
    print()
    print("Usage: nc.py -t target_host -p port")
    print("-l --listen                    - listen on [host]:[port] for incoming connections")
    print("-e --execute file_to_run        - excute to given file upon receiving a coonection")
    print("-c --command                    - initialize a command shell")
    print("-u --upload destination        - upon receiving connection upload a file and write to [destination]")
    print()
    print()
    print("Client Examples:")
    print("./.py -t 202.100.1.224 -p 5555")
    print("./nc.py -t 202.100.1.224 -p 5555 -u \'upload_src.txt\'")
    print("./nc.py -t 202.100.1.224 -p 5555")
    print("Server Examples:")
    print("./nc.py -l -p 5555 -c")
    print("./nc.py -l -p 5555 -u \'upload_dst.txt\'")
    print("./nc.py -l -p 5555 -e \'cat /etc/passwd\'")