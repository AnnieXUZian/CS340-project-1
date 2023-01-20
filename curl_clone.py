import sys
import socket
import collections
import os

#Use sys to get the http link passed in
input_address = str(sys.argv[1])

if("https://" in input_address):
    sys.stderr.write("Cannot intake an https")
    sys.exit(1)
    
if (input_address[-1]=="/"):
    input_address = input_address[:-1]

HOST = input_address[7:]  #sys.argv[1]- gets us the address  str()- makes it a string [7:]- gets rid of http://
PORT = 80

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect_ex((HOST, PORT)) # connect to the host


website_name = "GET / HTTP/1.1\r\nHost:"+HOST+"\r\n\r\n"

sock.send(website_name.encode('utf-8'))

response = sock.recv(4096)

data = response.decode()



start_index = data.find("<body>")
end_index = data.find("</body>")

output_message = "Header:"+HOST+"\n"+data[start_index:end_index+7]
sys.stdout.write(output_message)


#if (start_index == -1):
#     #error


if ("200 OK" in data): 
    sys.exit(0)
else:
    sys.exit(1)









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

# while http_client.response.is_redirect and num_redirects <= 10:
# Do work ()
# num_redirects += 1
# if num_redirects > 10:
#         print("Too many redirects", file=sys.stderr)
#         sys.exit(1)

#send a request with socket