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

    
    
    
    try:
        fp=open(message,'r')
    except:
        conn.send('HTTP/1.0 404 Not Found\r\n'.encode('utf-8'))
    else:
        if not (message[-4:]=='.htm' or message[-5:]=='.html'):
            conn.send('HTTP/1.0 403 Forbidden\r\n'.encode('utf-8'))
        else:
            contentH='HTTP/1.0 200 OK\r\n' + 'Content-Length: '+str(os.path.getsize("./"+message)) + \
            '\r\nContent-Type:text/html; charset=UTF-8\r\n\r\n'
            conn.send(contentH.encode())
            contentB=fp.read()
            conn.sendall(contentB.encode('utf-8'))
    
    
    conn.close()
