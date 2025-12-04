import sys
import os
import random
import string
from socket import *
import threading
client = {}

def client_handler(client_socket, clients): 

    client_socket.send("Enter username:")
    username = client_socket.recv(1024).decode()
    welcome_message = f"Welcome {username} to the chatroom!"
    while True: 
        message = client_socket.recv(1024).decode()
        if message:
            full_message = f"{username}: {message}"
            print(full_message)
            for c in clients:
                if c != client_socket:
                    c.send(full_message.encode())
        else:
            print(f"{username} has disconnected.")
            break
    client_socket.close()
    clients.remove(client_socket)

def main(): 
    #create socket and bind

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('', 12345))  #bind to all interfaces, port 12345

    #listen for connections

    server_socket.listen(5)
    print("Server is listening for connections...")
    clients = []
    while True: 
        #accept connection
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established!")
        clients.append(client_socket)
        threading.Thread(target=client_handler, args=(client_socket,clients)).start()


