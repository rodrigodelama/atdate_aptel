# !/usr/bin/python3
# time_client.py

# AUTHOR: Rodrigo De Lama @rodrigodelama
#         100451775@alumnos.uc3m.es
# DESCRIPTION: Basic TIME client script based on the outline of RFC868


'''
Time since 00:00h 1/1/1900
Time since UNIX existance 2208988800 (1970)

In plain-text:
The server listens for a connection on port 37. When the connection
is established, the client must send an empty packet to which
the server returns a 32-bit time value (data) and closes the
connection.
'''

import sys # For commandline args
from socket import socket, getaddrinfo, SOCK_STREAM, AF_INET, gaierror #SOCK_STREAM is TCP, AF_INET is Addr. Fam. IPv4
from time import gmtime # The time.pyi library has this funtion to format secconds
import struct # To isolate our desired info from the packet with unpack()

# Define a buffer size for the 32 bit BIN number we will recieve
# 4 bytes * 8 bits/byte = 32 bits
BUFFSIZE = 4
# Substract 2 hours, to get (CEST +2 hours)
time_delta = 2208988800 - 3600*2 # epoch time - 2 hours


def get_current_time():
    # Filter input args or instruct usage
    if len(sys.argv) == 2:
        target = sys.argv[1]
    else:
        print("Input the IP address of the desired time server")
        print("Usage: %s <IP Address>\n" (sys.argv[0]))
        sys.exit(1)

    print("Attempting to connect to:", target)
    # Get address info in a "2D" tuple
    # Index [0] is the IP address of the desired hostname
    # Index [-1] is the definition of the Port No. where we will open our socket
    server = getaddrinfo(target, 37)[0][-1] # 2D 

    # Test print input address data:
    # (Format is: ('IP', PORT_NO) )
    # print(server)

    sockett = socket(AF_INET, SOCK_STREAM)
    try:
        sockett.connect(server)
    except socket.gaierror:
        print("Error")

    # If the connection succeeds, send the empty TCP message
    sockett.send(bytes(0))

    # Revieve the 4byte (32bit) current time data
    recv_data = sockett.recv(BUFFSIZE)
    # print(recv_data) # WHAT ENCODING IS THIS ??

    sockett.close() # Close the socket

    time_since_1970 = struct.unpack("!I", recv_data)[0] # https://docs.python.org/3/library/struct.hatl#struct.calcsize
    '''
    ! tranforms our data from the network order (BE) to x64 (LE)
    I means unsigned integer (4bytes: the buffer size we need)

    (the combination of both "!I" is equivalent to ntohs in C)
    '''

    time_since_1970 -= time_delta
    actual_time = gmtime(time_since_1970) # easier to yank the desired data and format it
    print(actual_time) # We shall format this data below

def format_time(actual_time):
    at = actual_time
    s = str("Current time: " + get_week_day(at[6]) + ", " + str(at[0]) + "-" + str(at[1]) + "-" + str(at[2]) + ", " + str(at[3]) + ":" + str(at[4]) + ":" + str(at[5]))
    return s

def main():
    get_current_time()

if __name__ == "__main__":
    main()
