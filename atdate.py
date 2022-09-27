# !/usr/bin/python3
# atdate.py

from socketserver import UDPServer
import sys # For commandline args
from socket import socket, getaddrinfo, AF_INET, SOCK_DGRAM, SOCK_STREAM, gaierror #SOCK_STREAM is TCP, AF_INET is Addr. Fam. IPv4
from time import gmtime # The time.pyi library has this funtion to format secconds
import struct # To isolate our desired info from the packet with unpack()

# Define a buffer size for the 32 bit BIN number we will recieve
# 4 bytes * 8 bits/byte = 32 bits
BUFFSIZE = 4
# Substract 2 hours, to get (CEST +2 hours)
time_delta = 2208988800 - 3600*2 # GMT - 2 hours for CET

# Constants for sepparating the different modes
TCP = "TCP"
UDP = "UDP"

def get_current_time(target, mode, port):
    print("Attempting to connect to:", target)
    # Get address info in a "2D" tuple
    # Index [0] is the IP address of the desired hostname
    # Index [-1] is the definition of the Port No. where we will open our socket
    server = getaddrinfo(target, port)[0][-1] # 2D 

    # Test print input address data:
    # (Format is: ('IP', PORT_NO) )
    # print(server)

    if (mode == UDP):
        # We will create the socket w/ SOCK_DGRAM - UDP sends datagrams
        sockett = socket(AF_INET, SOCK_DGRAM)
    elif(mode == TCP):
        # We will create the socket w/ SOCK_STREAM - TCP sends streams of bytes
        sockett = socket(AF_INET, SOCK_STREAM)
    
    try:
        sockett.connect(server)
    except gaierror:
        print("Error")

    # If the connection succeeds, send the empty message (by the users choice: UDP/TCP)
    sockett.send(bytes(0))

    # Revieve the 4byte (32bit) current time data
    recv_data = sockett.recv(BUFFSIZE)
    # print(recv_data) # FIXME: WHAT ENCODING IS THIS ??

    sockett.close() # Close the socket

    time_since_1970 = struct.unpack("!I", recv_data)[0] # https://docs.python.org/3/library/struct.hatl#struct.calcsize
    '''
    ! tranforms our data from the network order (BE) to x64 (LE)
    I means unsigned integer (4bytes: the buffer size we need)

    (the combination of both "!I" is equivalent to ntohs in C)
    '''

    time_since_1970 -= time_delta
    actual_time = gmtime(time_since_1970) # easier to yank the desired data and format it
    # print(actual_time) # We shall format this data below
    print(format_time(actual_time))
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

def time_server(listening_port):
    # TODO:
    print("TIME server running on port ", listening_port)

def main():
    # client or server functionality menu should be here
    # also filter parameters here

    # program shall launch like this:
    '''
    atdate [-s serverhost] [-p port] [-m cu | ct | s ] [-d]

    -s serverhost
    hostname || IP

    -p port selection
    if port is specified 
    elif no port is specified use 37

    -m
    cu: el programa arranca en modo consulta funcionando como cliente UDP.
    ct: el programa arranca en modo consulta funcionando como cliente TCP.
    s: el programa arranca en modo servidor.
    Si no se especifica la opción -m, el programa arranca en modo consulta UDP,
        es decir: -m cu.

    -d: modo depuración. Mostrará trazas adicionales para la depuración del
    programa.
    
    Si alguno de los parámetros opcionales necesarios para la ejecución no se
    proporciona por línea de comandos, se tomarán los valores por defecto. (-m cu -p 37)
    '''
    # Filter input args or instruct usage
    if len(sys.argv) >= 7:
        print("Error: Too many input args")
        print("Input the IP address, and the desired protocol to contact the time server")
        print("Usage: " + sys.argv[0] + " <IP Address> <Protocol: UDP/TCP>\n" )
        sys.exit(1)
    elif len(sys.argv) == 3:
        target = sys.argv[1]
        mode = sys.argv[2] # TEMPORARY
        port = 37 # Default port -> TEMPORARY
    else:
        print("Input the IP address, and the desired protocol to contact the time server")
        print("Usage: " + sys.argv[0] + " <IP Address> <Protocol: UDP/TCP>\n" )
        sys.exit(1)
    
    '''
    if (-m == cu) mode = UDP
    elif (-m == ct) mode = TCP
    '''
    
    # Modo consulta UDP: -m cu

    # get_current_time(target, UDP)
    # Modo consulta TCP: -m ct
    get_current_time(target, mode, port)

    # Modo servidor: -m s
    # TODO:
    # time_server(listening_port)

if __name__ == "__main__":
    while True:
        try:
            main()
        except KeyboardInterrupt:
            print("\nSIGINT received, closing program")
            sys.exit(1)
