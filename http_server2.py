#server
import socket
import sys
import os
import select
import queue

PORT=int(sys.argv[1])
SERVER=socket.gethostbyname(socket.gethostname())
ADDR=("",PORT)

server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#server.setblocking(0)
server.bind(ADDR)
server.listen(5)

inputs=[server]
outputs=[]
message_queues={}


while True:
    readable,writable,exceptional=select.select(inputs,outputs,inputs)

    for s in readable:#handle inputs
        if s is server:#ready to accept a connection
            conn,addr=s.accept()
            #print(' connection from',addr,file=sys.stderr)
            #conn.setblocking(0)
            inputs.append(conn)#add to list of inputs to monitor
            #give connection a queue for data
            message_queues[conn]=queue.Queue()
        else: #connected client has sent data
            data=s.recv(1024) #recieve
            if data:
                #print('received {!r} from{}'.format(data,s.getpeername()),file=sys.stderr)
                message_queues[s].put(data)#place on the queue
                if s not in outputs:
                    outputs.append(s)#add output channels for response
            else:#disconencted
                #print(' closing',addr,file=sys.stderr)
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()

                del message_queues[s]

    for s in writable:
        try:
            next_msg=message_queues[s].get_nowait()
        except queue.Empty:
            #print(' ',s.getpeername(),'queue empty',file=sys.stderr)
            outputs.remove(s)
        else:
            #print(' sending{!r} from{}'.format(data,s.getpeername()),file=sys.stderr)
            message=next_msg.decode(errors= 'ignore')
            try:
                sIndex=message.find("Get")
            except:
                pass
            else:
                message=message[sIndex+6:]
                eIndex=message.find(" ")
                message=message[:eIndex]

                
                try:
                    fp=open(message,'r')
                except:
                    s.send('HTTP/1.0 404 Not Found\r\n'.encode('utf-8'))
                    inputs.remove(s)
                    if s in outputs:
                        outputs.remove(s)
                    s.close()
                else:
                    fp=open(message,'r')
                    if not (message[-4:]=='.htm' or message[-5:]=='.html'):
                        s.send('HTTP/1.0 403 Forbidden\r\n'.encode('utf-8'))
                        inputs.remove(s)
                        if s in outputs:
                            outputs.remove(s)
                        s.close()
                        continue
                    contentH='HTTP/1.0 200 OK\r\n' + 'Content-Length: '+str(os.path.getsize("./"+message)) + \
                    '\r\nContent-Type:text/html; charset=UTF-8\r\n\r\n'
                    s.send(contentH.encode())
                    contentB=fp.read()
                    s.sendall(contentB.encode('utf-8'))
                    
    for s in exceptional:
        print("exceptional")
        #print('exception condition on',s.getpeername(),file=sys.stderr)
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
                
    


