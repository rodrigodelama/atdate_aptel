# !/usr/bin/python3
# TIME.py

# AUTHOR: Rodrigo De Lama @rodrigodelama
#         100451775@alumnos.uc3m.es
# DESCRIPTION: Basic TIME client script based on the outline of RFC868

# Time since 00:00h 1/1/1900
# Time since UNIX existance 2208988800

# When used via TCP the time service works as follows:
#   S: Listen on port 37 (45 octal).
# U: Connect to port 37.
#   S: Send the time as a 32 bit binary number.
# U: Receive the time.
# U: Close the connection.
#   S: Close the connection.

# The server listens for a connection on port 37.  When the connection
# is established, the server returns a 32-bit time value and closes the
# connection.  If the server is unable to determine the time at its
# site, it should either refuse the connection or close it without
# sending anything.

# Open TCP connexion at port 37 of input IP
# Recieve the time
# Check for a reasonable difference (check era)
# Ask again if not correct
# Close conn


import sys # For commandline args
import time
import struct
from socket import getaddrinfo, socket, SOCK_STREAM, AF_INET, gethostbyname

# Define a buffer size for the 32 bit BIN number we will recieve
BUFSIZE = 4 # 4 bytes * 8 bits/byte = 32 bits

#if len(sys.argv) == 2:
#    target = sys.argv[1]
#else:
#    print("Input the IP address of the desired time server\n")
#    print("Usage: %s <IP Address>\n" % (sys.argv[0]))
#    sys.exit(1)

target = "time-a.timefreq.bldrdoc.gov"

# Open a socket at the inputted IP address, Port 37

clientSocket = socket(AF_INET, SOCK_STREAM)
print("Attempting to connect to:", target)

target_ip = gethostbyname(target) # Resolves both hostnames and IPs
print(target_ip) # Test print

getaddrinfo(target_ip, 37)
clientSocket.connect((target_ip, 37)) # 37 is the dedicated TIME port

while True:
    try:
        ping_TIME_server = ""
        s = clientSocket.send(ping_TIME_server.encode())
        if s < len(ping_TIME_server):
            print("Just", s, "bytes out of", len(ping_TIME_server), "sent")

        time = clientSocket.recv(BUFSIZE) # Recieves an X (int) number of bytes
        #if time < bytearray(BUFSIZE):

        print(time)
        #print(time.resolve())
        #print("decoded: ", time.decode())
        if not time:
            print("Broken TCP connection")
            break
    except KeyboardInterrupt:
        print("\nInterrupted by CTRL-C")
        break
clientSocket.close() # Close the socket
