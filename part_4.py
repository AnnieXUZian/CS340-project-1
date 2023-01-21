#server
import socket
import sys
import os
import json

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

    print(message)
    
    if (message[-4:-1]=='.htm' or message[-5:-1]=='.html'):
        conn.send('400 Bad Request'.encode('utf-8'))
        continue  
    
    mIndex=message.find('?')
    operation=message[:mIndex]
    if operation !='product':
        conn.send('404 Not Foound'.encode('utf-8'))
        continue
    message=message[mIndex+1:]
    if message=='':
       conn.send('400 Bad Request'.encode('utf-8')) 
    result=1
    i=1
    values=[]
    while True:
        
        tIndex=message.find('&')
        if(tIndex==-1):
            temp=message
            i=0
        else:
            temp=message[:tIndex]
            message=message[tIndex+1:]
            
        
        equal=temp.find('=')
        if(equal==-1):
            value=temp
        else:
            value=temp[equal+1:]
            
        try:
            value=float(value)
        except:
            conn.send('400 Bad Request'.encode('utf-8'))
        else:
            values.append(value)
            result=result*value

        if i==0:
            break
            
    if result==float('inf')
        result="inf"
            
    retu=json.dumps({"operation":"product","operands":values,"result":result},indent=4)
    
    conn.send(retu.encode('utf-8'))
    
    conn.close()
