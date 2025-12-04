import sys
import os
import random
import string
import threading
from socket import *

#1. Create TCP client Socket
client_socket = socket(AF_INET, SOCK_STREAM)

#2. connect to the server using the server's IP address and port
server_IP_address = "127.0.0.1"
server_port= 12345
client_socket.connect((server_IP_address, server_port))

#3. Display the client's local address and port information
print("Successfully connected to server from: ", client_socket.getsockname())

#4. Start a background thread to continuously: Recievee messages from the server and display received messages to the user
def continuously_receive_messages():
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if msg:
                print("\n" + msg)
            else:
                print("Server closed connection.")
                client_socket.close()
                break
        except:
            print("Error receiving message.")
            client_socket.close()
            break
threading.Thread(target=continuously_receive_messages, daemon=True).start()
            
#5 + 6. In the main thread, repeatedly: accept the use inout from the keyboard and send the typed message to the server + close
while True:
    try:
        message = input("")
        client_socket.send(message.encode())
    except:
        print("Connection error.")
        client_socket.close()
        break

