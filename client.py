#!/usr/bin/env python3

import socket
import sys

if len(sys.argv) != 2:
    print("usage: client.py host_name")
    sys.exit(1)

HOST = sys.argv[1]
PORT = 65429

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        s.connect((HOST, PORT))

        data = s.recv(2048).decode('utf-8')

        user_name = input(data)
        s.sendall(bytes(user_name, 'utf-8'))
        print(s.recv(2048).decode('utf-8'))

        # user_in = input('$>')
