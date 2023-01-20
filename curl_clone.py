import sys
import socket
import collections
import os

counter = 10
PORT = 80


input_address = str(sys.argv[1])
output_message = "Host:..."+"\n"
sys.stdout.write(output_message)



def get_html(input_address,requests):
#Use sys to get the http link passed in
    
    if requests==10:
        sys.exit(1)
        
    PORT = 80
    
    if("https://" in input_address): #check for https
      sys.stderr.write("Cannot intake an https")
      sys.exit(1)

    if (input_address[-1]=="/"):#with / at the end of the URL
        input_address = input_address[:-1]
        
    if(':' in input_address[7:]): #with a port number
        portP=(input_address[7:]).find(':')
        PORT=input_address[portP+8:-1]
        PORT=int(PORT)
        input_address=input_address[:portP+7]

    HOST = input_address[7:]  #sys.argv[1]- gets us the address  str()- makes it a string [7:]- gets rid of http://

    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    sock.connect_ex((HOST, PORT)) # connect to the host
    website_name = "GET / HTTP/1.1\r\nHost:"+HOST+"\r\n\r\n"

    sock.send(website_name.encode('utf-8')) #send the URL

    response=sock.recv(4096) #get the response
    while True:
        data=sock.recv(4096)
        if not data:
            break
        else:
            response = response+data
            
    data = response.decode()  ## we have our response!

    place=data.find("<") #beginning of the body part

    http_response_code = data[9:data.find("\n")]

    if ("200" in http_response_code):
        print(data[place:])
        system.exit(0)
 

    if "301" in http_response_code:
        loc_index = data.find("Location:")
        temp_url = data[loc_index+10:]
        end_index = temp_url.find("\n")
        new_url = temp_url[:end_index]
        sys.stderr.write("Redirected to:"+new_url)
        requests=requests+1
        get_html(new_url,requests+1)
            
    if "302" in http_response_code:
        requests=requests+1
        loc_index = data.find("Location:")
        temp_url = data[loc_index+10:]
        end_index = temp_url.find("\n")
        new_url = temp_url[:end_index]
        sys.stderr.write("Redirected to:"+new_url)
        get_html(new_url,requests+1)


        
    status=http_response_code[:3]

    if int(status)>=400:
        sys.exit(1)


get_html(input_address,requests=0)
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
