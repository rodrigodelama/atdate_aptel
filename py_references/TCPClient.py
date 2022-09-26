#!/usr/bin/python3
#TCPClient.py

import sys
from socket import socket, SOCK_STREAM, AF_INET

BUFSIZE = 1024

if len(sys.argv) == 3:
    host = sys.argv[1]
    port = int(sys.argv[2])
else:
    print("usage: %s <host> <port>\n" % (sys.argv[0]))
    sys.exit(1)

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((host, port))

while True:
    try:
        message = input()
        s = clientSocket.send(message.encode())
        if s < len(message):
            print("Just", s, "bytes out of", len(message), "sent") 
        message = clientSocket.recv(BUFSIZE)
        if not message:
            print("Broken TCP connection")
            break
        print(message.decode())
    except KeyboardInterrupt:
        print("\nInterrupted by CTRL-C")
        break
clientSocket.close()
