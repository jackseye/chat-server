#!/usr/bin/env python3
import sys
import os
import socket
import subprocess
import threading

HOST = '0.0.0.0'
PORT = int(sys.argv[1])
BUFF = 2048

class Client:
    """
    class to represent chat users

    ...

    Attributes
    ----------
    name : str
        the name the user chooses to be known by
    addr : tuple
        the user's ip address
    conn : socket
        the socket connecting the user
    available: bool
        true when user is not in chat, false otherwise

    """
    def __init__(self, name, addr, conn):
        self.name = name
        self.addr = addr
        self.conn = conn
        self.available = True
        self.chat_thread = None


class Chat:
    """
    class to represent active chats

    ...

    Attributes
    ----------
    caller : Client
        the client that initiated the chat
    participants : list of Clients
        the client that the caller invited to the chat

    Methods    
    -------
    run_chat()
        invites client to join chat, gives each client a seperate thread to send/recieve, and monitors threads
    handle_client(sending=Client)
        handles message receiving and sending for each client. Exits when client chooses or is only client left in chat 

    """
    def __init__(self, calling, participants):
        self.caller = calling
        self.participants = participants

    def run_chat(self):
        #sending invitations and checking responses
        for participant in self.participants:
            participant.conn.sendall(bytes("talk request from " + self.caller.name + ". Accept? Y/N", 'utf-8'))

            resp = participant.conn.recv(BUFF).decode('utf-8').split(':')[1].lower()
            
            if resp != 'y' and resp != 'yes':
                self.caller.conn.sendall(bytes(participant.name + " has declined the chat.", 'utf-8'))
                participant.available = True
                self.participants.remove(participant)

        #at least one client accepted invitation. starting chat
        if len(self.participants) > 0:
            #adding caller to list of participants who recieve messages in chat
            self.participants.append(self.caller)
        
            threads = []
            for participant in self.participants:
                participant.chat_thread = threading.Thread(target=self.handle_client, args=(participant,))
                participant.chat_thread.start()

            #monitoring chat for exiting clients
            while len(self.participants) > 0:
                for participant in self.participants:
                    if not participant.chat_thread.is_alive():
                        #sending exited participant back to main server loop
                        participant.available = True
                        participant.chat_thread = None
                        self.participants.remove(participant)
        else:
            #no clients accepted chat. sending calling client back to main server loop
            self.caller.available = True            

    def handle_client(self, sending):
        #alerts other clients that sending client has entered chat
        for participant in self.participants:
                if participant != sending:
                    participant.conn.sendall(bytes(sending.name + " has joined the chat", "utf-8"))

        data = sending.conn.recv(BUFF)
        while b'exit' not in data and len(self.participants) > 1:
            for participant in self.participants:
                if participant != sending:
                    participant.conn.sendall(data) 
            data = sending.conn.recv(BUFF)

        #alerting remaining clients that sending client has left the chat
        if len(self.participants) > 1:
            for participant in self.participants:
                if participant != sending:
                    participant.conn.sendall(bytes(sending.name + " has left the chat", "utf-8"))

        #alerting client when they are the only one left in chat
        else:
            sending.conn.sendall(bytes("Everyone else has left. Ending chat now", "utf-8"))

class Server:
    """
    class to represent the server

    ...

    Attributes
    ----------
    host : str
        the host for the socket
    port : int
        the port on which the server listens for client connections
    sock : socket
        the socket used to communicate with clients
    clients : dictionary, key: str, val: Client
        list of all clients currently connected to server

    Methods    
    ------- 
    run() 
        creates and bind socket, then listens for incoming client connections
    one_client_con()
        creates new client object for incoming connections and handles client commands
    """

    def __init__(self):
        self.host = HOST
        self.port = PORT
        self.clients = {}

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen()

        while True:
            conn, addr = self.sock.accept()
            print('connected by', addr)
            thread = threading.Thread(target=self.handle_clients, args=(conn, addr,))
            thread.start()

    def handle_clients(self, conn, addr):
        conn.sendall(b"Enter your name: ")
        client_name = conn.recv(BUFF).decode('utf-8')

        while client_name in self.clients:
            conn.sendall(b"Name already taken. Enter name: ")
            client_name = conn.recv(BUFF).decode('utf-8')

        client = Client(client_name, addr, conn)    
        self.clients[client_name] = client

        welcome = "Welcome, " + client_name + "\nEnter 'talk <user>' to talk to another user\nEnter exit to disconnect"
        conn.sendall(welcome.encode('utf-8'))

        while client_name in self.clients and client.available:
            data = conn.recv(BUFF).decode('utf-8')

            if 'exit' in data:
                conn.sendall(b"Goodbye")
                self.clients.pop(client.name)
                conn.close()

            elif 'talk' in data:
                participants = []
                for recipient in data.split(' ')[1:]:
                    #client has not joined server
                    if recipient not in self.clients:
                        conn.sendall(bytes(recipient + " is not online.", 'utf-8'))
                    #client has joined server and is in chat
                    elif not self.clients[recipient].available:
                        conn.sendall(bytes(recipient + " is busy.", 'utf-8'))
                    else:
                        self.clients[recipient].available = False
                        participants.append(self.clients[recipient])

                client.available = False

                #starting chat with all available participants
                chat = Chat(client, participants)
                chat.run_chat()

            else:
                conn.sendall(bytes("\nEnter 'talk <user>' to talk to another user\nEnter exit to disconnect", 'utf-8'))

if __name__ == "__main__":
    server = Server()

    server.run()