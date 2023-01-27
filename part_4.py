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
    
    message=conn.recv(4096).decode('utf-8')
    sIndex=message.find("Get")
    
    message=message[sIndex+6:]
    eIndex=message.find(" ")
    message=message[:eIndex]
    
    mIndex=message.find('?')
    if(mIndex==-1):
        operation=message
    else:
        operation=message[:mIndex]
        
    if operation !='product':
        conn.send('HTTP/1.0 404 Not Found\r\n'.encode('utf-8'))
        continue
    
    if mIndex==(len(message)-1) or mIndex==-1:
        conn.send('HTTP/1.0 400 Bad Request\r\n'.encode('utf-8'))
        continue
    
    message=message[mIndex+1:]
    

    result=1
    i=1
    bre=0
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
            float(value)
        except ValueError:
            conn.send('HTTP/1.0 400 Bad Request\r\n'.encode('utf-8'))
            bre=1
            break
        else:
            value=float(value)
            values.append(value)
            result=result*value

        if i==0:
            break
    if bre==1:
        continue
    if result==float('inf') or result==float('-inf'):
        result="inf"
    retu=json.dumps({"operation":"product","operands":values,"result":result},indent=2)

    contentH='HTTP/1.0 200 OK\r\n' + 'Content-Length: '+str(sys.getsizeof(retu)) + \
    '\r\nContent-Type:application/json; charset=UTF-8\r\n\r\n'
    conn.send(contentH.encode())
    
    conn.sendall(retu.encode('utf-8'))
    
    conn.close()
