import socket
import select
import sys
from threading import Thread
import multiprocessing




def handle_loader(clients, load, ip, port):
    readload, _, _ = select.select(load, [], load, 0.5)
    print("Load Handler",readload)
    
    for loader in readload:
        loader.setblocking(True)
        data = loader.recv(1024)
        loader.setblocking(False)
        print("REACHED INSIDE LOADER")
        print(data)
        if data.decode('utf-8') =="CONNECTIONS":
            loader.send("{}".format(len(clients) - 1).encode('utf-8'))
        elif data.decode('utf-8')=="CONNINFO":
            loader.send("{} {}".format(ip, port).encode("utf-8"))


def handle_incoming_connection(clients, serverSocket):

    readclient, _, _  = select.select(clients, [], clients, 0.5)
    print("Client Reader", readclient)
    for client in readclient:
        if client == serverSocket:
            conn, addr = serverSocket.accept()
            conn.setblocking(False)
            clients.append(conn)
            
        else:
            break

def server_handler(ip, port):
   
    

    loadSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    loadSocket.connect(("localhost", 8888))
    loadSocket.send("SERVER".format(ip, port).encode('utf-8'))

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind((ip, port))
    serverSocket.setblocking(False)
    serverSocket.listen(25)
    
    clients = [serverSocket]
    load = [loadSocket]
    while True:
        
        threads = []
        q = multiprocessing.Queue()
        q.put(clients)
        t = multiprocessing.Process(target=handle_incoming_connection, args=[q, serverSocket], daemon=True)
        threads.append(t)
        t.start()

        t = multiprocessing.Process(target=handle_loader, args = [q, load, ip, port], daemon=True)
        threads.append(t)
        t.start()
        
        for t in threads:
            t.join()
        

        
if __name__ == "__main__":
    ip = sys.argv[1]
    port = int(sys.argv[2])
    server_handler(ip, port)