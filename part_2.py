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
    sIndex=message.find("Get")
    message=message[sIndex+6:]
    eIndex=message.find(" ")
    message=message[:eIndex]

    
    if not (message[-4:]=='.htm' or message[-5:]=='.html'):
        conn.send('403 Forbidden'.encode('utf-8'))
    else:
        try:
            fp=open(message,'r')
        except:
            conn.send('404 Not Found'.encode('utf-8'))
        else:
            content=fp.read()
            conn.send(content.encode('utf-8'))
    
    
    conn.close()
