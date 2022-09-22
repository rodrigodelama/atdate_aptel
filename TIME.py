# !/usr/bin/python3
# TIME.py

# AUTHOR: Rodrigo De Lama @rodrigodelama
#         100451775@alumnos.uc3m.es
# DESCRIPTION: Basic TIME client script based on the outline of RFC868


# When used via TCP the time service works as follows:
#   S: Listen on port 37 (45 octal).
# U: Connect to port 37.
#   S: Send the time as a 32 bit binary number.
# U: Receive the time.
# U: Close the connection.
#   S: Close the connection.

#   The server listens for a connection on port 37.  When the connection
#   is established, the server returns a 32-bit time value and closes the
#   connection.  If the server is unable to determine the time at its
#   site, it should either refuse the connection or close it without
#   sending anything.

# Open TCP connexion at port 37 of input IP

# Recieve the time
# Check for a reasonable difference (check era)
# Ask again if not

# close conn


import sys
from socket import socket, SOCK_STREAM, AF_INET

# Define a buffer size for the 32 bit BIN number we will recieve
# 4 bytes * 8 bits/byte = 32 bits
BUFSIZE = 4

if len(sys.argv) == 2:
    host = sys.argv[1]
else:
    print("Input the IP address of the desired time server\n")
    print("Usage: %s <IP Address>\n" % (sys.argv[0]))
    sys.exit(1)

# Open a socket at the inputted IP Add, Port 37
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((host, 37)) # 37 is TIMEs dedicated port

while True:
    try:
        time = clientSocket.recv(BUFSIZE)
        print(time)
        if not time:
            print("Broken TCP connection")
            break
        print(time.decode())
    except KeyboardInterrupt:
        print("\nInterrupted by CTRL-C")
        break

# Close the socket
clientSocket.close()
