"""This python file contains the code for the implementation of the client side of the char application."""

import socket
import select
import string
import errno
import kbhiT
import pyDH
import sys, os
import clientfunctions as f
import time
import random
from threading import Thread
HEADER_LENGTH = 10



IP = "127.0.0.1"
PORT = 13248
CLIENT_KEY = str(pyDH.DiffieHellman())

# using random.choices()
# generating random strings


def accept_messages(port):
    cmSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cmSocket.bind(("localhost", int(port)))
    cmSocket.setblocking(False)
    cmSocket.listen()
    msList=[cmSocket]
    readers,_,_ = select.select(msList, [], [])

    for sock in readers:
        if sock == cmSocket:
            
            conn, addr = cmSocket.accept()
            
            
            # Receive our "header" containing username length, it's size is defined and constant
            conn.setblocking(True)
            username_header = conn.recv(HEADER_LENGTH)
            
            # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            # Convert header to int value
            username_length = int(username_header.decode('utf-8').strip())

            # Receive and decode username
            username = conn.recv(username_length).decode('utf-8')
            
            # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
            message_header = conn.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = conn.recv(message_length).decode('utf-8')
            
            # Print message
            print(f'{username} > {message}')
            print(f" > ", end='')


def send_messages(my_username, client_socket):
    while True:
        #kb = kbhiT.KBHit()

        if True:
            # Wait for user to input a message
            recvID = input(f'{my_username} > RecieverID >')
            message = input(f'{my_username} > Message >')

            if message.find("EXITNOW") != -1:
                client_socket.close()
                break

            # If message is not empty - send it
            if message:

                # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
                recvID = recvID.encode('utf-8')
                recv_header = f"{len(recvID):<{HEADER_LENGTH}}".encode('utf-8')
                client_socket.send(recv_header + recvID)
                
                message = message.encode('utf-8')
                message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                client_socket.send(message_header + message)
                

        
        
            
            continue



uport = sys.argv[1]

ClientKey = str(''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=16)))

# Connect to load balancer
client_socket = f.new_socket(IP, PORT)

# Asks loadbalancer to assign a server:
userclient = "USERCLIENT".encode('utf-8')
client_header = f"{len(userclient):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(client_header + userclient)
time.sleep(2.5)

# Receives new server details and connects to it
message_header = client_socket.recv(HEADER_LENGTH)
message_length = int(message_header.decode('utf-8').strip())
message = client_socket.recv(message_length).decode('utf-8')
message_list = message.split(':')
print(message_list)
client_socket.close()
client_socket = f.new_socket(message_list[0], int(message_list[1]))

user_wish = input("Do you want to SignUp (0) or Login (1)? ")
if user_wish == "0":
    my_username = input("Phone: ")
    my_pwd = input("New Password: ")

    # Store client key in a new file
    ClientKey = f.sign_up(client_socket, my_username, my_pwd, uport)
    print(ClientKey)
    dir = my_username
    parent_dir = '.'
    path = os.path.join(parent_dir, dir)
    os.mkdir(path)
    path = os.path.join(path, f"{my_username}_key.txt")
    file = open(path, 'w')
    file.write(str(ClientKey))
    file.close()

    
else : 
    my_username = input("Phone: ")
    my_pwd = input("Password: ")

    # Get stored client key!
    dir = my_username
    parent_dir = '.'
    path = os.path.join(parent_dir, dir)
    path = os.path.join(path, f"{my_username}_key.txt")
    file = open(path, 'r')
    ClientKey = file.readline()
    file.close()
    client_socket.setblocking(True)
    f.credential_login(client_socket, my_username, my_pwd, ClientKey, uport)
    data = client_socket.recv(1024).decode('utf-8')
    if data == "INVALID":
        print("Invalid Credentials")
        client_socket.close()
        sys.exit()

    elif data == "LOGGEDIN":
        print("Logged In!")

    client_socket.setblocking(False)



threads = []

t1 = Thread(target=accept_messages, args=[uport])
t1.start()
threads.append(t1)

t2 = Thread(target=send_messages, args = [my_username, client_socket])
t2.start()
threads.append(t2)

for t in threads:
    t.join()


    