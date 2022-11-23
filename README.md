# ChatterBox-CS251

#### CS-251 Autumn Semester Project 2022-23. Based on the concept of "FastChat".
#### Made by Aman, Aditya and Vijay.

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
Least Connections Algorithm:In this algorithm, traffic is directed to the server having the least traffic. This helps maintain the optimized performance, especially at peak hours by maintaining a uniform load at all the servers.

We are using the Least Connections Algorithm in our project. It is quite efficient as whenever a new request is made by a client, it selects the server with the least number of connections. This prevents any server from getting overloaded.


