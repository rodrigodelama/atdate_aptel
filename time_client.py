# !/usr/bin/python3
# time.py

# AUTHOR: Rodrigo De Lama @rodrigodelama
#         100451775@alumnos.uc3m.es
# DESCRIPTION: Basic TIME client script based on the outline of RFC868
#              When used via TCP the time service works as follows:
#               S: Listen on port 37 (45 octal).
#               U: Connect to port 37.
#               S: Send the time as a 32 bit binary number.
#               U: Receive the time.
#               U: Close the connection.
#               S: Close the connection.

'''
Time since 00:00h 1/1/1900
Time since UNIX existance 2208988800

The server listens for a connection on port 37.  When the connection
is established, the server returns a 32-bit time value and closes the
connection.  If the server is unable to determine the time at its
site, it should either refuse the connection or close it without
sending anything.

Open TCP connexion at port 37 of input IP
Recieve the time
Check for a reasonable difference (check era)
Ask again if not correct
Close connection
'''


import sys # For commandline args
from socket import socket, getaddrinfo, SOCK_STREAM, AF_INET, gaierror
import time
import struct # To isolate our desired info from the packet

# Substract 2 hours, so we get + 2 hours (CEST)
t_delta = 2208988800 - 3600*2 # epoch time - 2 hours


# Define a buffer size for the 32 bit BIN number we will recieve
BUFFSIZE = 4 # 4 bytes * 8 bits/byte = 32 bits

if len(sys.argv) == 2:
    target = sys.argv[1]
else:
    print("Input the IP address of the desired time server\n")
    print("Usage: %s <IP Address>\n" (sys.argv[0]))
    sys.exit(1)

print("Attempting to connect to:", target)

# Get address info
server_address = getaddrinfo(target, 37)[0][-1] # 2D Tuple, we select the two indexes we want (Ip, port)
#print(server_address) # Test print

# Open a socket at the inputted IP address, Port 37
sockett = socket(AF_INET, SOCK_STREAM)

try:
    sockett.connect(server_address) # 37 is the dedicated TIME port
except socket.gaierror:
    print("Error")

# If the connection succeeds, send the empty TCP message
sockett.send(bytes(0))

recv_data = sockett.recv(BUFFSIZE) # An int that represents a number of bytes

sockett.close() # Close the socket

time1970 = struct.unpack("!I", recv_data)[0]

time1970 -= t_delta
actual_time = time.gmtime(time1970)

print(actual_time)

print(recv_data)



'''

[(<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_DGRAM: 2>, 17, '', ('93.184.216.34', 80)),(<AddressFamily.AF_INET: 2>, <SocketKind.SOCK_STREAM: 1>, 6, '', ('93.184.216.34', 80)),(<AddressFamily.AF_INET6: 30>, <SocketKind.SOCK_DGRAM: 2>, 17, '', ('2606:2800:220:1:248:1893:25c8:1946', 80, 0, 0)),(<AddressFamily.AF_INET6: 30>, <SocketKind.SOCK_STREAM: 1>, 6, '', ('2606:2800:220:1:248:1893:25c8:1946', 80, 0, 0))]

'''