# Uncomment this to pass the first stage
import socket
import re
import sys 
import subprocess
import gzip


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
  print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
  server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
  while True:
    conn, addr = server_socket.accept() # wait for client
    httpString = conn.recv(500).decode()
    httpStringList = httpString.split('\r\n')
    httpVerbStringList = httpStringList[0].split()
    endpoint = httpVerbStringList[1]
    headerValueMap = dict()
    for keyValue in httpStringList[1:len(httpStringList)-1]:
        if keyValue != "":
           key,value = keyValue.split(":",1)
           headerValueMap[key.strip().lower()] = value.strip() 
        else:
           continue  
    if endpoint == "/"  :
       conn.send("HTTP/1.1 200 OK\r\n\r\n".encode())
    stringEchoMatched = re.search("(?<=/echo/)(\w+)", endpoint)
    stringuserAgentMatched = re.match(r"/user-agent$", endpoint)
    stringFileCheckMatched = re.search("(?<=/files/)(\w+)", endpoint)
    isValidEchoReq = httpVerbStringList[0] == "GET" and stringEchoMatched
    isValidEncoding = False
    try :
       encoding = headerValueMap["accept-encoding"] 
       if "gzip" in encoding.split(", ") :
            isValidEncoding = True
    except:
         pass
    isuserAgentReq = httpVerbStringList[0] == "GET" and stringuserAgentMatched
    isfileSearchReq = httpVerbStringList[0] == "GET" and stringFileCheckMatched
    isfilePostReq = httpVerbStringList[0] == "POST" and stringFileCheckMatched
    if isValidEchoReq:
       body = stringEchoMatched.group(0)
       length = len(body)
       contentType = "text/plain"
       encodingHeader= ""
       if isValidEncoding:
           encodingHeader = "Content-Encoding: gzip\r\n"
           body = gzip.compress(body.encode())
           resp = "HTTP/1.1 200 OK\r\n{0}Content-Type: text/plain\r\nContent-Length: {1}\r\n\r\n".format(encodingHeader,len(body))
           senddata = resp.encode()+body
       else:
           resp = "HTTP/1.1 200 OK\r\n{0}Content-Type: text/plain\r\nContent-Length: {1}\r\n\r\n{2}".format(encodingHeader,len(body),body)
           senddata = resp.encode()
       conn.send(senddata)
    elif isuserAgentReq:
       body = headerValueMap["user-agent"] 
       length = len(body)
       resp = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {0}\r\n\r\n{1}".format(length,body)
       conn.send(resp.encode())
    elif isfileSearchReq:
       filename = stringFileCheckMatched.group(0)
       if len(sys.argv)!=3 :
          conn.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
          return
       inputPath = sys.argv[2]
       filenameWithPath = inputPath +filename
       print(filenameWithPath)
       result = subprocess.run(['ls',filenameWithPath], stdout=subprocess.PIPE)
       file = result.stdout.decode('utf-8').split("\n")[0]
       if file != "":
            fd = open(filenameWithPath, "r")
            body = fd.read()
            length = len(body)
            resp = "HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {0}\r\n\r\n{1}".format(length,body)
            conn.send(resp.encode())
            fd.close()
       else:
          conn.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
    elif isfilePostReq:
       filename = stringFileCheckMatched.group(0)
       
       if len(sys.argv)!=3 :
          print("here")
          conn.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
          return
       inputPath = sys.argv[2]
       filenameWithPath = inputPath +filename
       
       fd = open(filenameWithPath, "w")
       fd.write(httpStringList[-1])
       conn.send("HTTP/1.1 201 Created\r\n\r\n".encode())
       fd.close()
    else: 
       conn.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())

if __name__ == "__main__":
    main()
