import socket
import select
import sys

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientSocket.connect(("localhost",8888))
clientSocket.sendall("ASSIGN".encode('utf-8'))
print("Client Connected")
msg = clientSocket.recv(1024).decode('utf-8').split()
read = [clientSocket]
print(msg)

alottedServer = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
alottedServer.connect((msg[1], int(msg[2])))
print ("Assigned to port {}".format([msg[2]]))
alottedServer.setblocking(False)
while True:
    readers, writers, errors = select.select([alottedServer], [], [], 0.5)
    
    for r in readers:
        if r == clientSocket:
            clientSocket.setblocking(True)
            msg = clientSocket.recv(1024).decode('utf-8').split()
            clientSocket.setblocking(False)
            print(msg)
            
        else:
            pass

