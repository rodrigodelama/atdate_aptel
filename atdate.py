# !/usr/bin/python3
# atdate.py

import sys # For commandline args
import os
from socket import socket, getaddrinfo, AF_INET, SOCK_DGRAM, SOCK_STREAM, gaierror #SOCK_STREAM is TCP, AF_INET is Addr. Fam. IPv4
from time import gmtime # The time.pyi library has this funtion to format secconds
import struct
from unittest.mock import DEFAULT # To isolate our desired info from the packet with unpack()
import datetime # Potentially for server
# Define a buffer size for the 32 bit BIN number we will recieve
# 4 bytes * 8 bits/byte = 32 bits
BUFSIZE = 4
# Substract 2 hours, to get (CEST +2 hours)
time_delta = 2208988800 - 3600*2 # GMT - 2 hours for CET

# Constants for sepparating the different mode
HOSTNAME = "-s"
MODE = "-m"
UDP = "cu"
TCP = "ct"
TIME_SERVER = "s"
PORT = "-p"
DEFAULT_PORT = 37
DEBUG = "-d"

# Server constants (from: TCPServer_conc.py)
SERV_BUFSIZE = 1024
BACKLOG = 10

def get_current_time(target, mode, port, debug_trigger):

    if debug_trigger == 1:
        print("Attempting to connect to:", target)
    # Get address info in a "2D" tuple
    # Index[0] (first) is the IP address of the desired hostname
    # Index[-1] (last) is the definition of the Port No. where we will open our socket
    server = getaddrinfo(target, port)[0][-1] # 2D 

    # Test print input address data:
    if debug_trigger == 1:
        # (Format is: ('IP', PORT_NO) )
        print(server)

    if (mode == UDP):
        if debug_trigger == 1:
            print("Attempting to open UDP socket")
        # We will create the socket w/ SOCK_DGRAM - UDP sends datagrams
        clientSocket = socket(AF_INET, SOCK_DGRAM)
    elif(mode == TCP):
        if debug_trigger == 1:
            print("Attempting to open TCP socket")
        # We will create the socket w/ SOCK_STREAM - TCP sends streams of bytes
        clientSocket = socket(AF_INET, SOCK_STREAM)
    
    try:
        clientSocket.connect(server)
        if debug_trigger == 1:
            print("Connected to TIME server!")
    except gaierror:
        print("Error")

    # ONLY UDP: If the connection succeeds, send the empty message
    if mode == UDP:
        clientSocket.send(bytes(0))
        if debug_trigger == 1:
            print("Sent empty UDP message (0bytes)")

    # Revieve the 4byte (32bit) current time data
    recv_data = clientSocket.recv(BUFSIZE)

    '''
    # POTENTIALLY UNNECESSARY
    while recv_data == "b\'\'": # FIXME: why is this happening ??
        try:
            recv_data = clientSocket.recv(BUFSIZE)
        except:
            struct.error
    '''
    
    if debug_trigger == 1:
        print("RAW recieved data:", recv_data) # TODO: WHAT ENCODING IS THIS ??

    clientSocket.close() # Close the socket
    if debug_trigger == 1:
            print("Succesful retreival: socket now closed")

    time_since_1970 = struct.unpack("!I", recv_data)[0] # https://docs.python.org/3/library/struct.html
    if debug_trigger == 1:
        print("time_since_1970 struct (tuple pos[0]):", time_since_1970)
    '''
    # FIXME: sometimes, mainly while running TCP, we get an error while unpacking "struct.error: unpack requires a buffer of 4 bytes"
    ! tranforms our data from the network order (BE) to x64 (LE)
    > is for a generic transformation from 
    I means unsigned integer (4bytes: the buffer size we need)

    (the combination of both "!I" is equivalent to ntohs in C)
    '''

    time_since_1970 -= time_delta
    actual_time = gmtime(time_since_1970) # easier to yank the desired data and format it
    if debug_trigger == 1:
            print("Unformatted time:", actual_time) # We will format this data below
            print("Formatted time:")
    print(format_time(actual_time))
    if debug_trigger == 1:
            print("Success!")
    exit(0) # End program after succesful TIME request

def format_time(actual_time):
    at = actual_time
    s = str(weekday(at[6])+" "+month(at[1])+" "+str(at[2])+" "+
            str(at[3])+":"+str(at[4])+":"+ str(at[5])+" CET "+str(at[0]))
    return s

def weekday(day):
    d = ''
    # no "switch" in python
    if(day == 0):
        d = 'Mon'
    elif(day == 1):
        d = 'Tue'
    elif(day == 2):
        d = 'Wed'
    elif(day == 3):
        d = 'Thu'
    elif(day == 4):
        d = 'Fri'
    elif(day == 5):
        d = 'Sat'
    elif(day == 6):
        d = 'Sun'
    return d

def month(month):
    m = ''
    if(month == 1):
        m = 'Jan'
    elif(month == 2):
        m = 'Feb'
    elif(month == 3):
        m = 'Mar'
    elif(month == 4):
        m = 'Apr'
    elif(month == 5):
        m = 'May'
    elif(month == 6):
        m = 'Jun'
    elif(month == 7):
        m = 'Jul'
    elif(month == 8):
        m = 'Aug'
    elif(month == 9):
        m = 'Sep'
    elif(month == 10):
        m = 'Oct'
    elif(month == 11):
        m = 'Nov'
    elif(month == 12):
        m = 'Dec'
    return m

def time_server(listening_port, debug_trigger):
    # TODO:
    if(debug_trigger == 1):
        print("TIME server running on port", listening_port)
    
#
# From TCPServer_conc.py
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', listening_port))
    serverSocket.listen(BACKLOG)

    try:
        (connectionSocket, client_addr) = serverSocket.accept()
        if os.fork() == 0:
            # child process
            mytime = datetime.now()
            message = struct.pack("<I", mytime) # Potentally will have to send in big endian.
                                                # also try ! might work since its a network script
            serverSocket.send(message)
            serverSocket.close()
            
            # message = connectionSocket.recv(SERV_BUFSIZE) # Big buffer so we may concurrently serve many clients
            '''
            while message:
                print(message.decode())
                connectionSocket.send(message)
                message = connectionSocket.recv(SERV_BUFSIZE)
            '''

            # we have to check for a conn in TCP
            #
            # we have to check to recieve empty UDP messages
            
            connectionSocket.close()
            os._exit(0)
        else:
            # parent process
            connectionSocket.close()
    except:
        serverSocket.close()
#
#

def main():
    # client or server functionality menu should be here
    # also filter parameters here

    # program shall launch like this:
    '''
    atdate [-s serverhost] [-p port] [-m cu | ct | s ] [-d]

    -m: operating mode
    cu: el programa arranca en modo consulta funcionando como cliente UDP.
    ct: el programa arranca en modo consulta funcionando como cliente TCP.
    s: el programa arranca en modo servidor.
    Si no se especifica la opción -m, el programa arranca en modo consulta UDP,
        es decir: -m cu.

    -s: serverhost
    hostname || IP

    -p: port selection
    if port is specified 
    elif no port is specified use 37

    -d: modo depuración. Mostrará trazas adicionales para la depuración del
    programa.
    
    Si alguno de los parámetros opcionales necesarios para la ejecución no se
    proporciona por línea de comandos, se tomarán los valores por defecto. (-m cu -p 37)
    '''
    # Filter input args or instruct usage

    if len(sys.argv) >= 9: # we should have at most 9 args (0-8)
        print("Error: Too many input args")
        print("Input the IP address, and the desired protocol to contact the time server")
        print("Usage: %s -s <Hostname/IP Address> -m <Mode> <Port> -d <Debug>\n" % (sys.argv[0]))
        print("Hostname/IP Address: input your desired TIME server")
        print("Mode: cu Makes the TIME request via UDP")
        print("      ct Makes the TIME request via TCP")
        print("Port: input the desired port for the TIME_SERVER mode, in client mode it will always default to 37")
        print("Debug: input \"-d\" to trigger debug mode (log all steps taken by the program onto the terminal)")
        sys.exit(1)

    ## The following are the various conditions to interpret our input with flags
    # We will filter argv positions for -m -s -p and -d
    
    # Debugger Activation
    try:
        if (sys.argv.index(DEBUG)): # DEBUG means -d
            debug_trigger = 1
    except ValueError:
        debug_trigger = 0

    # Hostname validity check, and assignment to target
    try:
        if (sys.argv.index(HOSTNAME)): # HOSTNAME means -s

            if debug_trigger == 1:
                print("Hostname input position in argv[] is:", sys.argv.index(HOSTNAME)+1)
                print("Target (hostname) has been identified as:", sys.argv[sys.argv.index(HOSTNAME)+1])

            target = sys.argv[sys.argv.index(HOSTNAME)+1]
    except ValueError:
        try:
            if (sys.argv.index(MODE)): # MODE means -m
                print("Error: You must at least enter a HOSTNAME to run with default settings, as a client making a UDP request")
                sys.exit(1)
        except ValueError:
            if not (sys.argv.index(UDP) or sys.argv.index(TCP)):
                print("Error: You must select SERVER mode (-m s) if you do not input a hostname")
                sys.exit(1)

    # Mode selection and default behaviour programmed
    try:
        if (sys.argv.index(MODE)):
            mode = sys.argv[sys.argv.index(MODE)+1]
            if debug_trigger == 1:
                print("Mode has been identified as:", mode)
    except ValueError:
        mode = UDP # Default: UDP client

    '''
    # NEW PARAMETER EXAMPLE
    new_param_x = ""
    try:
        if (sys.argv.index("-x")):
            mode = sys.argv[sys.argv.index(MODE)+1]
            if debug_trigger == 1:
                print("The new parameter is:", new_param_x)
    except ValueError:
        mode = UDP # Default: UDP client
    '''

    # Port selection for server and default behaviour programmed
    try:
        if (sys.argv.index(PORT)): # PORT means -p
            port = sys.argv[sys.argv.index(PORT)+1]
    except ValueError: 
            port = DEFAULT_PORT # Default: Port 37

    ## Program launch
    # Client
    if mode == UDP or mode == TCP:
        get_current_time(target, mode, DEFAULT_PORT, debug_trigger)
    # Server
    elif mode == TIME_SERVER:
        time_server(port, debug_trigger)
    # Error
    else:
        print("Error: Invalid operation mode")
        sys.exit(1)

# This is how we execute main
# The code below means we want this script to be executed, signaling Python that it's NOT a library
if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("\nSIGINT received, closing program")
            sys.exit(1)
