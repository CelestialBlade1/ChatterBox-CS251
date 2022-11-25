import socket
import select
import string
import errno
import kbhiT
import sys, os
import pyDH
import clientfunctions as f
import time
import random
HEADER_LENGTH = 10



IP = "127.0.0.1"
PORT = 13248
CLIENT_KEY = str(pyDH.DiffieHellman())

# using random.choices()
# generating random strings

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
    ClientKey = f.sign_up(client_socket, my_username, my_pwd)
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
    f.credential_login(client_socket, my_username, my_pwd, ClientKey)
    data = client_socket.recv(1024).decode('utf-8')
    if data == "INVALID":
        print("Invalid Credentials")
        client_socket.close()
        sys.exit()

    elif data == "LOGGEDIN":
        print("Logged In!")

    client_socket.setblocking(False)

    


while True:
    print("Choose one of the following commands :-")
    print("READ MESSAGE OF USER (READUSER)")
    print("READ MESSAGE OF USER (READGROUP)")
    print("READ MESSAGE TO USER (SENDUSER)")
    print("SEND MESSAGE TO GROUP (SENDGROUP)")
    command = input("Enter your Command")
    

    if command == "READUSER":
        pass
    elif command == "READGROUP":
        pass
    elif command == "SENDUSER":
        reciever = input("Enter Phone No.")
        kb = kbhiT.KBHit()
        if reciever and kb.kbhit():
            # Wait for user to input a message
                message = input(f'{my_username} > ')
                if message.find("EXITNOW") != -1:
                    client_socket.close()
                    break

                # If message is not empty - send it
                if message:
                    message = reciever +"~"+ message
                    # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
                    
                    message = message.encode('utf-8')
                    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                    client_socket.send(message_header + message)
    elif command == "SENDGROUP":
        reciever = input("Enter Group Name")
        kb = kbhiT.KBHit()
        if reciever and kb.kbhit():
            # Wait for user to input a message
                message = input(f'{my_username} > ')
                if message.find("EXITNOW") != -1:
                    client_socket.close()
                    break

                # If message is not empty - send it
                if message:
                    message = reciever +"~"+ message
                    # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
                    
                    message = message.encode('utf-8')
                    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                    client_socket.send(message_header + message)
        if kb.kbhit():
            # Wait for user to input a message
                message = input(f'{my_username} > ')
                if message.find("EXITNOW") != -1:
                    client_socket.close()
                    break

                # If message is not empty - send it
                if message:
                    message = reciever +"~"+ message
                    # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
                    
                    message = message.encode('utf-8')
                    message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
                    client_socket.send(message_header + message)
        
                

    try:
        # Now we want to loop over received messages (there might be more than one) and print them
        while True:

            # Receive our "header" containing username length, it's size is defined and constant
            username_header = client_socket.recv(HEADER_LENGTH)

            # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
            if not len(username_header):
                print('Connection closed by the server')
                sys.exit()

            # Convert header to int value
            username_length = int(username_header.decode('utf-8').strip())

            # Receive and decode username
            username = client_socket.recv(username_length).decode('utf-8')

            # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            # Print message
            print(f'{username} > {message}')

    except IOError as e:
        # This is normal on non blocking connections - when there are no incoming data error is going to be raised
        # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
        # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
        # If we got different error code - something happened
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error: {}'.format(str(e)))
            sys.exit()

        # We just did not receive anything
        continue

    except Exception as e:
        # Any other exception - something happened, exit
        print('Reading error: {}'.format(str(e)))
        sys.exit()