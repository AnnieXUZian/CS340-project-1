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
server.bind(ADDR)
server.listen(5)

inputs=[server]
outputs=[]
message_queues={}


while True:
    print('waiting for the next event',file=sys.stderr)
    readable,writable,exceptional=select.select(inputs,outputs,inputs)

    for s in readable:#handle inputs
        if s is server:#ready to accept a connection
            conn,addr=s.accept()
            #print(' connection from',addr,file=sys.stderr)
            conn.setblocking(0)
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
            message=next_msg.decode('utf-8')
            try:
                sIndex=message.find("Get")
            except:
                pass
            else:
                message=message[sIndex+6:]
                eIndex=message.find(" ")
                message=message[:eIndex]

                if (message[-4:-1]=='.htm' or message[-5:-1]=='.html'):
                    s.send('403 Forbidden'.encode('utf-8'))
                else:
                    try:
                        fp=open(message,'r')
                        s.send(fp.read().encode('utf-8'))
                    except:
                        s.send('404 Not Found'.encode('utf-8'))
    for s in exceptional:
        #print('exception condition on',s.getpeername(),file=sys.stderr)
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()

                
    

