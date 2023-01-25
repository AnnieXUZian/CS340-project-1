import sys
import socket
import collections
import os


def print_body(input_data, host_name):  #helper function to print only the body out
  start_index = input_data.find("<")

  output_message = "Header:"+host_name+"\n"+input_data[start_index:]

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
        port = address[end_p+1:end_i]
        host = address[:end_p]

    #print ("path = " + path + " host = " + host + " port = "+ str(port))

    return path, host, port


    


#Use sys to get the http link passed in
input_address = str(sys.argv[1])    #gets us the address





def try_recursion(web_name, counter):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #makes a socket

    if("https://" in web_name):
      print("Cannot intake an https", file = sys.stderr)
      sys.exit(1)

    # if (counter == 0):
    #     print("Too many redirects", file = sys.stderr)
    #     sys.exit(5)

    list_of_args = (understand_address(web_name)) 

    path1 = list_of_args[0]
    host1 = list_of_args[1]
    port1 = list_of_args[2]
    if (isinstance(port1, str)):
        port1 = int(port1)

    print("Host = ", host1)                #prints HOST

    sock.connect_ex((host1, port1)) # connect to the host

    website_name = "GET /"+path1+" HTTP/1.0\r\nHost:"+host1+ ":" + str(port1) +"\r\n\r\n"

    sock.send(website_name.encode('utf-8'))

    response=sock.recv(4096) #get the response
    
    while True:
        data=sock.recv(4096)
        if not data:
            break
        else:
            response = response+data

    sock.close()

    data = response.decode('utf-8')  ## we have our response!
    http_response_code = data[9:data.find("\n")]
    
    content_type=data[data.find("Content-Type")+14:data.find("Content-Type")+23]
    if not content_type=='text/html': #check content type
        sys.exit(1)

    if ("200" in http_response_code):
        print_body(data, host1)
        sys.exit(0)

    if("301" in http_response_code):
        counter = counter - 1
        if (counter==0):
          print("Too many redirects", file = sys.stderr)
          sys.exit(1)
        loc_index = data.find("Location:")
        new_data = data[loc_index+10:]
        end_index = new_data.find("\n")
        new_url = new_data[:end_index-1]
  
        print("redirected to "+new_url, file = sys.stderr)

        try_recursion(new_url, counter)

    if("302" in http_response_code):
        counter = counter - 1
        if (counter==0):
            print("Too many redirects", file = sys.stderr)
            sys.exit(1)
        loc_index = data.find("Location:")
        new_data_1 = data[loc_index+10:]
        end_index = new_data_1.find("\n")
        new_url = new_data_1[:end_index-1]

        print("redirected to "+new_url, file = sys.stderr)

        try_recursion(new_url, counter)

    if("4" in http_response_code):
        print_body(data, host1) # print the respond body to stdout
        sys.exit(3)
 


    


try_recursion(input_address, 10)
