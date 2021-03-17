#!/usr/bin/env python3

import socket
import sys


def conn_to_server(socket):
    data = s.recv(2048).decode('utf-8')

    user_name = input(data)
    s.sendall(bytes(user_name, 'utf-8'))
    data = s.recv(2048).decode('utf-8')

    while 'Name already taken' in data:
        user_name = input(data)
        s.sendall(bytes(user_name, 'utf-8'))
        data = s.recv(2048).decode('utf-8')

    print(data)
        
def request_talk(ip):
    s.sendall('ip')

def accept_talk():
    pass

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("usage: client.py <host-ip> <port-number>")
        sys.exit(1)

    HOST = sys.argv[1]
    PORT = int(sys.argv[2])

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        conn_to_server(s)
        print("Enter \'talk <user-ip>\' to talk to another user\nEnter exit to disconnect")
        
        while input('>') != 'exit':
            print('hello')
