import sys
import os
import random
import string
from socket import *
import threading

def client_handler(client_socket, clients,username): 
    while True: 
        try: 
            msg = client_socket.recv(1024).decode()
            if not msg:
                break
        except:
            break
        if msg.startswith("@"): 
            #private message
            split_msg = msg.split(" ",1)
            target_username = split_msg[0][1:]
            message = split_msg[1]
            if target_username in clients: 
                target_socket = clients[target_username]
                target_socket.sendall(
                    f"[{username} -> you]: {message}".encode()
                )
            else: 
                client_socket.sendall("User not found.".encode())
        else:
            client_socket.sendall(f"use correct format (@username message)".encode())
    del clients[username]
    client_socket.close()
    

def main(): 
    #create socket and bind

    server_socket = socket(AF_INET, SOCK_STREAM)
    server_socket.bind(('', 12345))  #bind to all interfaces, port 12345

    #listen for connections

    server_socket.listen(5)
    print("Server is listening for connections...")
    clients = {}
    while True: 
        #accept connection
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} has been established!")

        #request and recieve username
        client_socket.send("Enter username:".encode())
        username = client_socket.recv(1024).decode().strip()

        #add username and socket to clients dictionary
        clients[username] = client_socket
        print(f"Username {username} has joined the chat.")
        
        #start client handler thread
        threading.Thread(target=client_handler, args=(client_socket,clients,username), daemon=True).start()


