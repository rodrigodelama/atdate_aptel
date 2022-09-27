# !/usr/bin/python3
# atdate.py

import sys # For commandline args
import os
from socket import socket, getaddrinfo, AF_INET, SOCK_DGRAM, SOCK_STREAM, gaierror #SOCK_STREAM is TCP, AF_INET is Addr. Fam. IPv4
from time import gmtime # The time.pyi library has this funtion to format secconds
import struct
from unittest.mock import DEFAULT # To isolate our desired info from the packet with unpack()

# Define a buffer size for the 32 bit BIN number we will recieve
# 4 bytes * 8 bits/byte = 32 bits
BUFSIZE = 4
# Substract 2 hours, to get (CEST +2 hours)
time_delta = 2208988800 - 3600*2 # GMT - 2 hours for CET

# Constants for sepparating the different modes
#TCP = "TCP"
#UDP = "UDP"


HOSTNAME = "-s"
MODE = "-m"
UDP = "cu"
TCP = "ct"
TIME_SERVER = "s"
PORT = "-p"
DEFAULT_PORT = 37
DEBUG = "-d"

# Server constants
SERV_BUFSIZE = 1024
BACKLOG = 10

def get_current_time(target, mode, port, debug_trigger):

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

    # If the connection succeeds, send the empty message (by the users choice: UDP/TCP)
    clientSocket.send(bytes(0))
    if debug_trigger == 1:
            print("Sent empty UDP/TCP message (0bytes)")

    # Revieve the 4byte (32bit) current time data
    recv_data = clientSocket.recv(BUFSIZE)
    if debug_trigger == 1:
            print("RAW recieved data: ", recv_data) # TODO: WHAT ENCODING IS THIS ??

    clientSocket.close() # Close the socket
    if debug_trigger == 1:
            print("Socket closed")

    time_since_1970 = struct.unpack("!I", recv_data)[0] # https://docs.python.org/3/library/struct.html
    '''
    ! tranforms our data from the network order (BE) to x64 (LE)
    I means unsigned integer (4bytes: the buffer size we need)

    (the combination of both "!I" is equivalent to ntohs in C)
    '''

    time_since_1970 -= time_delta
    actual_time = gmtime(time_since_1970) # easier to yank the desired data and format it
    if debug_trigger == 1:
            print("Complete formatted time: ", actual_time) # We will format this data below
    print(format_time(actual_time))
    if debug_trigger == 1:
            print("Program success! Closing now...")
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
    print("TIME server running on port ", listening_port)

#
# From TCPServer_conc.py
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', listening_port))
    serverSocket.listen(BACKLOG)

    try:
        connectionSocket, addr = serverSocket.accept()
        if os.fork() == 0:
            # child process
            serverSocket.close()
            message = connectionSocket.recv(SERV_BUFSIZE) # Big buffer so we may concurrently serve many clients
            while message:
                print(message.decode())
                connectionSocket.send(message)
                message = connectionSocket.recv(SERV_BUFSIZE)
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

# function next() usually used by previously running iter(), but in our case it is not needed

    # filter argv positions for -m -s -p and -d
    my_port = DEFAULT_PORT
    if len(sys.argv) >= 7: # we should have at most 7 args (0-6)
        print("Error: Too many input args")
        print("Input the IP address, and the desired protocol to contact the time server")
        print("Usage: %s -s <Hostname/IP Address> -m <Mode> <Port> -d <Debug>\n" % (sys.argv[0]))
        print("Hostname/IP Address: input your desired TIME server")
        print("Mode: cu Makes the TIME request via UDP")
        print("      ct Makes the TIME request via TCP")
        print("Port: input the desired port for the TIME_SERVER mode, in client mode it will always default to 37")
        print("Debug: input \"-d\" to trigger debug mode (log all steps taken by the program onto the terminal)")
        sys.exit(1)
    
    argv_str = " ".join(sys.argv)
    #print("argv_str: ", argv_str)

    try:
        if (sys.argv.index(DEBUG)):
            debug_trigger = 1
    except ValueError:
        debug_trigger = 0
    try:
        if (sys.argv.index(HOSTNAME)): # -s means HOSTNAME
            # print(sys.argv.index(HOSTNAME))
            target = sys.argv[sys.argv.index(HOSTNAME)+1]
            # print(sys.argv[sys.argv.index(HOSTNAME)+1])
    except ValueError:
        try:
            if (sys.argv.index(MODE)):
                print("Error: You must at least enter a HOSTNAME to run with default settings, as a client making a UDP request")
                sys.exit(1)
        except ValueError:
            if not (sys.argv.index(UDP) or sys.argv.index(TCP)):
                print("Error: You must select SERVER mode (-m s) if you do not input a hostname")
                sys.exit(1)

    try:
        if (sys.argv.index(MODE)):
            mode = sys.argv[sys.argv.index(MODE)+1]
    except ValueError:
        mode = UDP # Default: UDP client

    try:
        if (sys.argv.index(PORT)):
            port = sys.argv[sys.argv.index(PORT)+1]
    except ValueError: 
            port = 37 # Defaults: UDP client

    if (debug_trigger == 1):
        print("argv_str: ", argv_str)
        print("Target: ", target)
        print("Mode: ", mode)

    if mode == UDP or mode == TCP:
        get_current_time(target, mode, DEFAULT_PORT, debug_trigger)
    elif mode == TIME_SERVER:
        time_server(port, debug_trigger)

'''
OLD MANUAL STARTUP
    if (len(sys.argv) == 3):
        target = sys.argv[1]
        mode = sys.argv[2] # TEMPORARY
        # port = 37 # Default port -> TEMPORARY
        
        if (mode == CU):
            mode = UDP
            # Modo consulta UDP: -m cu
            get_current_time(target, mode, 37, debug_trigger)
        elif (mode == CT):
            mode = TCP
            # Modo consulta TCP: -m ct
            get_current_time(target, mode, 37, debug_trigger)
        elif (mode == TIME_SERVER):
            # Modo servidor: -m s
            # TODO:
            listening_port = port
            time_server(listening_port)
        else:
            print("Error: Invalid operation mode")
            sys.exit(1)
    else:
        print("Input the IP address, and the desired protocol to contact the time server")
        print("Usage: %s <IP Address> <Protocol: UDP/TCP>\n" % (sys.argv[0]))
        sys.exit(1)
'''
# Means we want this script to be executed, and that it's not a library.
if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("\nSIGINT received, closing program")
            sys.exit(1)
