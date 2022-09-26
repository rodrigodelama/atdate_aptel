#!/usr/bin/python3
#TCPServer_conc.py

import sys
import os
from socket import socket, SOCK_STREAM, AF_INET

BUFSIZE = 1024
BACKLOG = 10

if len(sys.argv) == 2:
    port = int(sys.argv[1])
else:
    print("usage: %s <port>\n" % (sys.argv[0]))
    sys.exit(1)

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', port))
serverSocket.listen(BACKLOG)
while True:
    try:
        connectionSocket, addr = serverSocket.accept()
        if os.fork() == 0:
            # child process
            serverSocket.close()
            message = connectionSocket.recv(BUFSIZE)
            while message:
                print(message.decode())
                connectionSocket.send(message)
                message = connectionSocket.recv(BUFSIZE)
            connectionSocket.close()
            os._exit(0)
        else:
            # parent process
            connectionSocket.close()
    except KeyboardInterrupt:
        print("\nInterrupted by CTRL-C")
        break
serverSocket.close()
