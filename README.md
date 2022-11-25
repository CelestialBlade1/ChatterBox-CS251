# ChatterBox-CS251

#### CS-251 Autumn Semester Project 2022-23. Based on the concept of "FastChat".
#### All code updates have been done on branches!
#### Made by Aman, Aditya and Vijay.

## Dependencies:-
    1. Working installation of Postgres (run on 15) and a database named ChatDB.
    2. pyDH library for end to end encryption of messages.
    3. Select Library for multiplexing of sockets.
    4. kbhit library to detect keyboard hits.

## The Basic Idea:
![image](https://user-images.githubusercontent.com/105475348/203462031-232b8b42-2596-4dc7-a262-75d1321301b6.png)

The active clients are alloted servers through the Load Balancer, and begin chatting. The User session begins after credential verification. User messages are routed through servers and the database is used to find the current server of any User as well as to find the relevenat members of a group. Messages are encrypted and new login sessions result in Locked updates of Database.
The File System and Databse maintain the basic information critical for the system.

### The Basic Group Chat:
The idea is to use Select.select() a python method that makes an OS call. It is efficient than multi-threading for larger operations. 

Each user can broadcast a message on the group chat and it is received by all others.

### The Basic Database:
![image](https://user-images.githubusercontent.com/105475348/203462455-ebc58041-5458-4f91-8b3e-8f7546db7004.png)

It will become more advanced as the Databse and Chat are merged.

### Load Balancing:
Round Robin Algorithm: In this algorithm, we send a request to the load balancer to assign us the a server to evenly distribute the load. This is done by selecting the next server in a cycle to which the the previous client was connected.

We are using the Round Robin Algorithm in our project. Whenever a new request is made by a client, it selects the server the next server in the cycle . This prevents any server from getting overloaded by selecting a server in the cycle with lesser connections.

### Instructions to run code.
    0. First open the load balancer as
    
    ```
    python loadbalancer.py ROUNDROBIN
    ```
    
    1. Next you want to launch the servers as:
    
    ```
    python server.py <localhost_port_no>
    ```
    
    such as
    
    `
    python server.py 8887
    `
    
    2. Now the clients can be launched
    
    ```
    python client.py <localhost_port_no>
    ```
    
    3. The client interfaces are ready to be used. Enter recipient user IDs to send DMs.




