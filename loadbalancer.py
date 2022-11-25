"""This class code for the implementation of a node balancer using ROUND ROBIN ALGORITHM.
"""

import socket, sys
import select
import kbhiT as kb
import time
import serverfunctions
from clientfunctions import Crypt

ALGO = sys.argv[1]
if len(sys.argv) != 2:
    assert "Correct usage: \npython loadbalancer.py <name_of_algorithm>"
    sys.exit(1)

elif ALGO == "ROUNDROBIN" or ALGO == "LEASTCONNECTIONS":
    pass
else:
    assert "Please choose correct Algorithm: \nROUNDROBIN \nor LEASTCONNECTIONS"
    sys.exit(1)

HEADER_LENGTH = 10
ROUNDROBIN_COUNT = 0
IP = "127.0.0.1"
PORT = 13248

# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
lb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# SO_ - socket option
# SOL_ - socket option level
# Sets REUSEADDR (as a socket option) to 1 on socket
lb_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind, so server informs operating system that it's going to use given IP and port
# For a server using 0.0.0.0 means to listen on all available interfaces, useful to connect locally to 127.0.0.1 and remotely to LAN interface IP
lb_socket.bind((IP, PORT))

# This makes server listen to new connections
lb_socket.listen()

# List of sockets for select.select()
sockets_list = [lb_socket]

# List of connected server - socket as a key, user header and name as data
server_connec = {}

print(f'Listening for connections on {IP}:{PORT}...')

# Handles message receiving

timeout = time.time()
while True:
    
    # Calls Unix select() system call or Windows select() WinSock call with three parameters:
    #   - rlist - sockets to be monitored for incoming data
    #   - wlist - sockets for data to be send to (checks if for example buffers are not full and socket is ready to send some data)
    #   - xlist - sockets to be monitored for exceptions (we want to monitor all sockets for errors, so we can use rlist)
    # Returns lists:
    #   - reading - sockets we received some data on (that way we don't have to check sockets manually)
    #   - writing - sockets ready for data to be send thru them
    #   - errors  - sockets with some exceptions
    # This is a blocking call, code execution will "wait" here and "get" notified in case any action should be taken
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)


    # Iterate over notified sockets
    for notified_socket in read_sockets:

        
        # If notified socket is a server socket - new connection, accept it
        if notified_socket == lb_socket:

            # Accept new connection
            # That gives us new socket - client socket, connected to this given client only, it's unique for that client
            # The other returned object is ip/port set
            in_socket, in_address = lb_socket.accept()

            # Client should send his name right away, receive it
            user = serverfunctions.receive_message(in_socket)

            # If False - client disconnected before he sent his name
            if user is False:
                continue
            
            if user['data'].decode('utf-8').find("SERVERTyu3349lkjn") != -1:
                # Add accepted socket to select.select() list
                sockets_list.append(in_socket)

                # Also save username and username header
                server_connec[in_socket] = ((in_address[0],user['data'].decode('utf-8').split(':')[1]),0)

                print('Accepted new connection from {}:{}, username: {}'.format(in_address[0],user['data'].decode('utf-8').split(':')[1], user['data'].decode('utf-8')))
                print(sockets_list)
            elif user['data'].decode('utf-8').find("USERCLIENTSd567po") !=-1:
                list1 = user['data'].decode('utf-8').split(':')
                for sock in sockets_list:
                    if list1[1] == server_connec[sock][0][1]:
                        server_connec[sock][1] -= 1

            elif user['data'].decode('utf-8') == "USERCLIENT":
                
                if ALGO=="ROUNDROBIN":
                    ROUNDROBIN_COUNT  = (ROUNDROBIN_COUNT+1)%len(sockets_list)
                    v = sockets_list[ROUNDROBIN_COUNT]
                    if v == lb_socket:
                        ROUNDROBIN_COUNT  = (ROUNDROBIN_COUNT+1)%len(sockets_list)
                        v = sockets_list[ROUNDROBIN_COUNT]
                    
                    usercl = f"{server_connec[v][0][0]}:{server_connec[v][0][1]}".encode('utf-8')
                    print(f"{server_connec[v][0][0]}:{server_connec[v][0][1]}")
                    cl_header = f"{len(usercl):<{HEADER_LENGTH}}".encode('utf-8')
                    in_socket.send(cl_header + usercl)
                    print ("Redirecting {}:{} to connect to {}:{}".format(in_address[0],server_connec[v][0][1],*server_connec[v][0]))
                elif ALGO == "LEASTCONNECTIONS":
                    min_cons = 10_000
                    for server in sockets_list:
                        if server == lb_socket:
                            continue
                        else:
                            if min_cons > server_connec[server][1]:
                                min_cons = server_connec[server][1]
                                min_server = server
                    usercl = f"{server_connec[server][0][0]}:{server_connec[server][0][1]}".encode('utf-8')
                    cl_header = f"{len(usercl):<{HEADER_LENGTH}}".encode('utf-8')
                    in_socket.send(cl_header + usercl)

                    
                    print ("Redirecting {}:{} to connect to {}:{}".format(*in_address,*server_connec[server][0]))
                else :
                    pass
            print(user['data'].decode('utf-8'))
        # Else existing socket is sending a message
        else:
            continue
            
            
    # It's not really necessary to have this, but will handle some socket exceptions just in case
    for notified_socket in exception_sockets:

        # Remove from list for socket.socket()
        sockets_list.remove(notified_socket)

        # Remove from our list of users
        del server_connec[notified_socket]