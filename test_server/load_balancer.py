import socket
import select

SERVER_PORTS = [8889, 8890, 8891, 8892]

def load_balancer(ip, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((ip, port))
    server.setblocking(False)
    server.listen(100)


    readers = [server]
    writers = []
    errors = [server]
    SERVER_ADDRESSES = []
    SERVERS = []
    
    print("Listening on the server")
    try:
        while True:
            readable, writable, error = select.select(readers, writers, readers, 1)
            print(readers)
            for s in readable:
                try: 
                    if s == server:
                        
                        conn, addr = server.accept()
                        conn.setblocking(False)
                        readers.append(conn)
                        
                        s.setblocking(True)
                        type = conn.recv(1024).decode('utf-8')
                        s.setblocking(False)
                        if type == "SERVER":
                            print("CONNECTED TO SERVER")
                            SERVERS.append(conn)
                            SERVER_ADDRESSES.append((conn, addr))
                        else:
                            print("CONNECTED TO USER")
                            print("ENTERING THIS LOOP")
                            if conn not in SERVERS:    
                                print("Shouldnt enter here")
                                min_addr = None
                                min_connections = 100000
                                for p in SERVERS:
                                    p.send("CONNECTIONS".encode('utf-8'))
                                    print("SENT A MESSAGE")
                                    p.setblocking(True)
                                    data = p.recv(1024)
                                    print("Number of Connections: ", data)
                                    p.setblocking(False)

                                    
                                    if int(data.decode('utf-8')) < min_connections:
                                        min_connections = int(data.decode('utf-8'))
                                        min_addr = [addr for addr in SERVER_ADDRESSES if addr[0] == p]
                                min_addr[0][0].setblocking(True)
                                min_addr[0][0].send("CONNINFO".encode('utf-8'))
                                
                                data = min_addr[0][0].recv(1024).decode('utf-8').split()
                                min_addr[0][0].setblocking(False)
                                print("New data", data)
                                conn.send("CONNECT {} {}".format(data[0], data[1]).encode('utf-8'))
                                
                                readers.remove(conn)
                                conn.close()
                        
                        
                        

                        #if addr[1] in SERVER_PORTS:
                        #    SERVERS.append(conn)
                        #    SERVER_ADDRESSES.append((conn, addr))
                    else:
                        pass

                
                finally:
                    pass
    #except Exception as e:
    #    print(e)
    #    server.close()
    finally:
        server.close()      

if __name__ == "__main__":
    load_balancer("localhost", 8888)
