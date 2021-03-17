#!/usr/bin/env python3

import os
import socket
import subprocess
import threading

HOST = '0.0.0.0'
PORT = 65426

#dict of clients
#key: client name
#value: [ip, port, logged_in]
clients = {}

def add_client(name, addr):
    #new client to be added
    if name not in clients:
        clients[name] = [addr[0], addr[1], True]
        #return None

    #returning client to be marked online
    elif (name in clients) and (addr[0]==clients[name][0]):
        clients[name][2] = True
        return 0

    #new client cannot use existing name
    else:
        return 1

def on_client_conn(conn):
    print('connected by', addr)
    
    conn.sendall(b'Enter your name: ')
    
    client_name = conn.recv(1024).decode('utf-8')

    added = add_client(client_name, addr)
    
    while added==1:
        conn.sendall(b'Name already taken. Enter name: ')
        client_name = conn.recv(1024).decode('utf-8')
        added = add_client(client_name, addr)
    
    if added==0:
        conn.sendall(b'Welcome back, ' + client_name.encode('utf-8'))
    else:
        conn.sendall(b'Welcome, ' + client_name.encode('utf-8'))

    data = conn.recv(1024).decode('utf-8')
    while data:
        if 'request:' in data:
            pass
        elif 'exit' in data:
            clients[name][2] = False
        else:
            pass
        
        data = conn.recv(1024).decode('utf-8')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=on_client_conn, args=(conn,))
        thread.start()
        
