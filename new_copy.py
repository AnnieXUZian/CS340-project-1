import sys
import socket
import collections
import os


def print_body(input_data, host_name):  #helper function to print only the body out
  start_index = input_data.find("<body>")
  end_index = input_data.find("</body>")

  output_message = "Header:"+host_name+"\n"+input_data[start_index:end_index+7]

  sys.stdout.write(output_message)


def understand_address(address):    #helper function to check that it's not https
    if("https://" in address):
      print("Cannot intake an https", file = sys.stderr)
      sys.exit(1)
    address = address[7:]
    end_i = address.find("/")
    end_p = address.find(":")
    host = address

    if ('/' not in address):
        path = ""
    if ('/' in address):
        path = address[end_i:]
        host = address[:end_i]
    if (":" not in address):
        port = 80
    if (":" in address):
        port = address[end_p:end_i]
        host = address[:end_p]

    print ("path = " + path + " host = " + host + " port = "+ str(port))

    return path, host, port


    


#Use sys to get the http link passed in
input_address = str(sys.argv[1])    #gets us the address



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #makes a socket



def try_recursion(web_name, counter):

    # if (counter == 0):
    #     print("Too many redirects", file = sys.stderr)
    #     sys.exit(5)

    list_of_args = (understand_address(web_name)) 

    path1 = list_of_args[0]
    host1 = list_of_args[1]
    port1 = list_of_args[2]


    print("Host = ", host1)                #prints HOST

    sock.connect_ex((host1, port1)) # connect to the host

    website_name = "GET /"+path1+" HTTP/1.0\r\nHost:"+host1+ ":" + str(port1) +"\r\n\r\n"

    sock.send(website_name.encode('utf-8'))

    response = sock.recv(4096)
    data = response.decode()  ## we have our response!
    http_response_code = data[9:data.find("\n")] 

    big_number = http_response_code.find(" ")
    actual_value = int(http_response_code[:big_number])
    print(http_response_code)
    print (actual_value)

    if ("200" in http_response_code):
        print_body(data, host1)
        sys.exit(0)

    while("301" in http_response_code):
        counter = counter - 1
        if (counter==0):
          print("Too many redirects", file = sys.stderr)
          sys.exit(1)
        loc_index = data.find("Location:")
        new_url = data[loc_index+10:]

        print(new_url)
  
        print("redirected to "+new_url, file = sys.stderr)

        try_recursion(new_url, counter)

    while("302" in http_response_code):
        counter = counter - 1
        if (counter==0):
            print("Too many redirects", file = sys.stderr)
            sys.exit(1)
        loc_index = data.find("Location:")
        new_url = data[loc_index+10:]
        print(new_url)

        print("redirected to "+new_url, file = sys.stderr)

        try_recursion(new_url, counter)

    if(actual_value>= 400):
        print("response over 400", file = sys.stderr)
        sys.exit(3)
 


    


try_recursion(input_address, 10)







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
