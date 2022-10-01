# !/usr/bin/python3
# atdate.py

import sys # For commandline args
import os
from socket import socket, getaddrinfo, AF_INET, SOCK_DGRAM, SOCK_STREAM, gaierror #SOCK_STREAM is TCP, AF_INET is Addr. Fam. IPv4
from time import gmtime, time # The time.pyi library has this funtion to format secconds
import struct # To isolate our desired info from the packet with unpack()
import time
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
BACKLOG = 10    # KINDA WORKS AS RECEPTION WINDOW SIZE:
                # the backlog parameter specifies the number
                # of pending connections the queue will hold.

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
        client_socket = socket(AF_INET, SOCK_DGRAM)
        # Only in UDP do we send the empty message to "server" (tuple with (addr,port))
        client_socket.sendto(bytes(0), server)
        if debug_trigger == 1:
            print("Sent empty UDP message (0bytes)")
        time_recieve(client_socket, debug_trigger)
        exit(0) # End program after succesful TIME request
    elif(mode == TCP):
        if debug_trigger == 1:
            print("Attempting to open TCP socket")
        # We will create the socket w/ SOCK_STREAM - TCP sends streams of bytes
        client_socket = socket(AF_INET, SOCK_STREAM)
        # Only in TCP do we handshake with the server
        try:
            client_socket.connect(server)
            if debug_trigger == 1:
                print("TCP handshake successful with TIME server!")
        except gaierror:
            print("Error")
            sys.exit(1)
        # Loop until SIGNINT - FIXME: BWOKEN 
        while True:
            try:
                time_recieve(client_socket, debug_trigger)
            except KeyboardInterrupt:
                print("\nSIGINT received, closing TCP connection")
                break

    # FIXME: see packet argparse
    # argparse.ArgumentParser

def time_recieve(client_socket, debug_trigger):
    # Revieve the 4byte (32bit) current time data
    # If UDP only ONCE else TCP constantly until SIGNINT
    recv_data = client_socket.recv(BUFSIZE)
    
    if debug_trigger == 1:
        print("RAW recieved data:", recv_data) # WHAT ENCODING IS THIS ??

    client_socket.close() # Close the socket
    
    if debug_trigger == 1:
            print("Succesful retreival: socket now closed")

    time_since_1970 = struct.unpack("!I", recv_data)[0] # https://docs.python.org/3/library/struct.html
    if debug_trigger == 1:
        print("time_since_1970 struct (tuple pos[0]):", time_since_1970)
    '''
    ! tranforms our data from the network order (BE) to x64 (LE)
    > is for a generic transformation from 
    I means unsigned integer (4bytes: the buffer size we need)

    (the combination of both "!I" is equivalent to ntohs in C)
    '''
    time_since_1970 -= time_delta
    # Carlos usa: time.ctime
    print( time.ctime(time_since_1970).replace(" 2022", " CET 2022") ) # Find a way to automate the year
    if debug_trigger == 1:
        print("Success!")

def time_server(listening_port, debug_trigger): # The server is concurrent
    if(debug_trigger == 1):
        print("TIME server running on port", listening_port)

    # From TCPServer_conc.py
    server_socket = socket(AF_INET, SOCK_STREAM)
    try:
        server_socket.bind(('', listening_port))
    except PermissionError:
        print("PermissionError: You must use \"sudo\" to launch your server on the default port 37")
        exit(1)
    server_socket.listen(BACKLOG)
    while True:
        connection_socket, client_addr = server_socket.accept()
        try:
            if os.fork() == 0:
                # child process
                mytime = int(time.time())
                if debug_trigger == 1:
                    print(type(mytime))
                    print(mytime)
                mytime += time_delta
                if debug_trigger == 1:
                    print("time plus time delta:", mytime)
                #maybe, time.ctime(secs) just does all the formatting for us.
                #instead of using "datetime", we will be using the "time" library, in which the function ctime() exists.
                message = struct.pack("!I", mytime) # Potentally will have to send in big endian. (yes)
                                                    # also try ! might work since its a network script
                server_socket.send(message)
                server_socket.close()
                connection_socket.close()
                os._exit(0)
                #NOTE: if we kill a socket with any port number, this port number will remain bloqued for some time (almost 2 mins), ther´s nothing we can do about it.
                # message = connection_socket.recv(SERV_BUFSIZE) # Big buffer so we may concurrently serve many clients
                
                # we have to check for a conn in TCP
                
                # we have to check to recieve empty UDP messages
            else:
                # parent process
                connection_socket.close()
        except KeyboardInterrupt:
            print("\nSIGINT received, closing server")
            break
    server_socket.close()

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
    
    if len(sys.argv) == 1: # no input args
        usage()
        sys.exit(1)

    if len(sys.argv) >= 9: # we should have at most 9 args (0-8)
        usage()
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
    except ValueError: # If a hostname is not entered -> must be in server "s" mode.
        if (sys.argv[sys.argv.index(MODE)+1] != TIME_SERVER): # MODE means -m
            print("Error: You must select SERVER mode (-m s) if you do not input a hostname")
            print("Additionally you may add a custom port number, otherwise it will run at the default port 37")
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
            port = int(sys.argv[sys.argv.index(PORT)+1])
    except ValueError:
            port = DEFAULT_PORT # Default: Port 37

    ## Program launch
    # Client
    if mode == UDP or mode == TCP:
        get_current_time(target, mode, port, debug_trigger)
    # Server
    elif mode == TIME_SERVER:
        time_server(port, debug_trigger)
    # Error
    else:
        print("Error: Invalid operation mode")
        sys.exit(1)

def usage():
    print("Usage: %s -s <Hostname/IP Address> -m <Mode> <Port> -d <Debug>" % (sys.argv[0]))
    print("Hostname/IP Address: input your desired TIME server")
    print("Mode: cu Makes the TIME request via UDP")
    print("      ct Makes the TIME request via TCP")
    print("Port: input the desired port for the TIME_SERVER mode, in client mode it will always default to 37")
    print("Debug: input \"-d\" to trigger debug mode (log all steps taken by the program onto the terminal)")

# This is how we execute main
# The code below means we want this script to be executed, signaling Python that it's NOT a library
if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("\nSIGINT received, closing program")
            sys.exit(1)
