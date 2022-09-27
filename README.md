# README

## Written by:
Rodrigo De Lama - @rodrigodelama - 100451775@alumnos.uc3m.es
Matías Scarpa - @Parsac2002 - 

## Description
The Python3 scrip "atdate.py" is designed to work both as a server, and a client (TCP/UDP) for the TIME protocol
- Basic TIME client script based on the outline of RFC868

- We took into account the following:
     - Time counted in seconds since 00:00h 1/1/1900
     - Seconds from 0 to UNIX (1970): 2208988800

     - The server will listen for connections on port 37. When a connection
       is established, the client must send an empty packet (TCP/UDP) to which
       the server will return a 32-bit number and close the connection.
