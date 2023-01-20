import sys
import socket
import collections
import os

#Use sys to get the http link passed in
input_string = sys.arg[1]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect((input_string, 80))

website_name = b"GET / HTTP/1.1\r\nHost:" + input_string +"\r\n\r\n"

sock.send(website_name)

response = sock.recv(4096)



print(response.decode())


#3 servers, 1 client- establishing a python file first



# if "http://" not in input_string[0:6]:
#         sys.stderr.write("not a valid website")
#         return 1

#     else:
#         sys.stdout.write("something")


#There should be a way to use status codes to help with the sorting of html stuff

#Open TCP connection to a port
#Then send the HTTP request message

#write a framework for client/server so it has the basic functionalities, can send a message
#Then, insert socket into the client, then build a bridge 


#Once a host recieves an IP address from the DNS, they can make a TCP connection to the HTTP server process located at port 80

#given http- an html file, print out body, response code, network layer is hard
#don't use high level packages- just low level sockets

#content length- for large pages, while true? Consider edge cases
#Show body of response- always print
#For 301, 302, also show an error
#how to parse http link for client, if it is redirecting, define path
#11th redirect is a 301- do we terminate?

while http_client.response.is_redirect and num_redirects <= 10:
Do work ()
num_redirects += 1
if num_redirects > 10:
        print("Too many redirects", file=sys.stderr)
        sys.exit(1)

#send a request with socket