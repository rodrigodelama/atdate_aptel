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
from socket import socket, SOCK_STREAM, AF_INET, gethostbyname

# Define a buffer size for the 32 bit BIN number we will recieve
# 4 bytes * 8 bits/byte = 32 bits
BUFSIZE = 4 # SHOULD IT BE SOMETHING ELSE ??

if len(sys.argv) == 2:
    target = sys.argv[1]
else:
    print("Input the IP address of the desired time server\n")
    print("Usage: %s <IP Address>\n" % (sys.argv[0]))
    sys.exit(1)

# if target ip is a hostname do an inverse DNS lookup to find out its IP address

# Open a socket at the inputted IP address, Port 37
clientSocket = socket(AF_INET, SOCK_STREAM)
print("Attempting to connect to:", target)
target_ip = gethostbyname(target) # Works for both hostnames and IPs
print(target_ip) # Test print
clientSocket.connect((target_ip, 37)) # 37 is TIMEs dedicated port

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
clientSocket.close() # Close the socket
