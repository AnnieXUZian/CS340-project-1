#server
import socket
import sys
import os

PORT=int(sys.argv[1])
SERVER=socket.gethostbyname(socket.gethostname())
ADDR=("",PORT)

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()
while True:
    conn,addr=server.accept()
    
    message=conn.recv(1024).decode('utf-8')
    print(message)
    sIndex=message.find("Get")
    message=message[sIndex+6:]
    eIndex=message.find(" ")
    message=message[:eIndex]

    if (message[-4:-1]=='.htm' or message[-5:-1]=='.html'):
        conn.send('403 Forbidden')
    else:
        try:
            fp=open(message,'r')
            conn.send(fp.read().encode('utf-8'))
        except:
            conn.send('404 Not Foound')
    #print(fp.read())
    
    
    conn.close()
