import sys
import socket
import collections
import os


def print_body(body_output):  #helper function to print only the body out
  body_output = body_output.decode(errors= 'ignore')
  end_index = body_output.find("</body>")

  output_message = body_output[:end_index]  #"Header:"+host_name+"\n"+

  sys.stdout.write(body_output + "\n")


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

    if("http://" not in web_name):
        print("need an http address", file = sys.stderr)
        sys.exit(2)

    if("https://" in web_name):
      print("Cannot intake an https", file = sys.stderr)
      sys.exit(1)

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

    response = b""

    while True:
        stuff = sock.recv(4096)
        response = response + stuff
        if not stuff:
            break

    body = response[response.find(b'\r\n\r\n') + 4:]
    
    response = response.decode(errors = 'ignore')

    data = response 

    sock.close()

    http_response_code = data[9:data.find("\n")] 

    content_type=data[data.find("Content-Type")+14:data.find("Content-Type")+23]
    if not content_type=='text/html': #check content type
        sys.exit(1)

    if ("200" in http_response_code):
        print_body(body)
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

    else:
        number = int(http_response_code [: http_response_code.find(" ")])
        if(number >= 400):
            print_body(data)
            #print("response over 400", file = sys.stderr)
            sys.exit(3)
 


    


try_recursion(input_address, 10)





