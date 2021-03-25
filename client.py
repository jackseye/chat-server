#!/usr/bin/env python3

import socket
import sys
import threading

BUFF = 2048

def conn_to_server(socket):
    data = s.recv(BUFF).decode('utf-8')

    user_name = input(data)
    s.sendall(bytes(user_name, 'utf-8'))
    data = s.recv(BUFF).decode('utf-8')

    while 'Name already taken' in data:
        user_name = input(data)
        s.sendall(bytes(user_name, 'utf-8'))
        data = s.recv(BUFF).decode('utf-8')

    print(data)

    return user_name

def recv_msg(s):
    data = s.recv(BUFF).decode('utf-8')
    while data:
        print(data + '\n>', end='')
        data = s.recv(BUFF).decode('utf-8')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("usage: client.py <host-ip> <port-number>")
        sys.exit(1)

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        user_name = conn_to_server(s)

        recv_msg = threading.Thread(target=recv_msg, args=(s,))
        recv_msg.start()

        while recv_msg.is_alive():
            user_in = input('>')
            s.sendall(bytes(user_name + ':' + user_in, 'utf-8'))
        
        print("Leaving the chat server")