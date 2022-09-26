#!/usr/bin/python3
#TCPServer_seq.py

import sys
from socket import socket, SOCK_STREAM, AF_INET

BUFSIZE = 1024
BACKLOG = 10

if len(sys.argv) == 2:
    port = int(sys.argv[1])
else:
    print("usage: %s <port>" % (sys.argv[0]))
    sys.exit(1)

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', port))
serverSocket.listen(BACKLOG)
while True:
    try:
        connectionSocket, addr = serverSocket.accept()
        message = connectionSocket.recv(BUFSIZE)
        while message:
            print(message.decode())
            connectionSocket.send(message)
            message = connectionSocket.recv(BUFSIZE)
        connectionSocket.close()
    except KeyboardInterrupt:
        print("\nInterrupted by CTRL-C")
        break
serverSocket.close()
