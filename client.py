#!/usr/bin/env python3

import socket
import sys

if len(sys.argv) != 3:
    print("usage: client.py <host-ip> <port-number>")
    sys.exit(1)

HOST = sys.argv[1]
PORT = int(sys.argv[2])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        data = s.recv(2048).decode('utf-8')

        user_name = input(data)
        s.sendall(bytes(user_name, 'utf-8'))
        data = s.recv(2048).decode('utf-8')
        while 'Name already taken' in data:
            user_name = input(data)
            s.sendall(bytes(user_name, 'utf-8'))
            data = s.recv(2048).decode('utf-8')
        print(data)
        

        # user_in = input('$>')
