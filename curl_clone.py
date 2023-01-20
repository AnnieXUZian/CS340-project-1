import sys
import socket
import collections
import os

counter = 10

def print_body(input_data):  #helper function to print only the body out
  start_index = input_data.find("<body>")
  end_index = input_data.find("</body>")

  output_message = "Header:"+HOST+"\n"+input_data[start_index:end_index+7]
  sys.stdout.write(output_message)


def check_https(address):    #helper function to check that it's not https
    if("https://" in address):
      sys.stderr.write("Cannot intake an https")
      sys.exit(1)

#Use sys to get the http link passed in
input_address = str(sys.argv[1])    
check_https(input_address)

if (input_address[-1]=="/"):
    input_address = input_address[:-1]

HOST = input_address[7:]  #sys.argv[1]- gets us the address  str()- makes it a string [7:]- gets rid of http://
PORT = 80

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect_ex((HOST, PORT)) # connect to the host



website_name = "GET / HTTP/1.1\r\nHost:"+HOST+"\r\n\r\n"

sock.send(website_name.encode('utf-8'))

response = sock.recv(4096)
data = response.decode()  ## we have our response!
http_response_code = data[9:data.find("\n")] 

if ("200" in http_response_code):
    print_body(data)

while ("301" in http_response_code and counter > 0):
    counter = counter - 1
    loc_index = data.find("Location:")
    new_url = data[loc_index+10:]
    end_index = new_url.find("\n")
    new_url = new_url[:end_index]
    sys.stderr.write("redirected to "+new_url)
    check_https(new_url)

while("302" in http_response_code and counter > 0):
    counter = counter - 1
    loc_index = data.find("Location:")
    new_url = data[loc_index+10:]
    end_index = new_url.find("\n")
    new_url = new_url[:end_index]
    print(new_url)

    




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