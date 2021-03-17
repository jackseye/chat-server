#!/usr/bin/env python3

import os
import socket
import subprocess
import threading

HOST = '0.0.0.0'
PORT = 65429

clients = {}

def add_client(name, addr):
    if name not in clients:
        clients[name] = addr
    else:
        return 1

def on_client_conn(conn):
    print('connected by', addr)
    while True:
        print("connecting")
        data = conn.recv(1024)
        if not data:
            break
        print("connected")

        conn.sendall(b'Enter your name: ')

        client_name = conn.recv(1024).decode('utf-8')
        
        if add_client(client_name, addr):
            conn.sendall(b'Name already taken. Enter name: ')
        else:
            conn.sendall(b'Welcome ' + client_name.encode('utf-8'))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=on_client_conn, args=(conn,))
        thread.start()
        
