# README

## Written by:
Rodrigo De Lama - @rodrigodelama - 100451775@alumnos.uc3m.es

Matías Scarpa - @Parsac2002 - 100451824@alumnos.uc3m.es

## Description
The Python3 scrip "atdate.py" is designed to work both as a server, and a client (UDP/TCP) for the TIME protocol

## Client modes
Basic TIME client script based on the outline of RFC868

We took into account the following:
  - Time counted in seconds since 00:00h 1/1/1900
  - Seconds from 0 to UNIX (1970): 2208988800

Tested with the provided addresses:
  - time-a.timefreq.bldrdoc.gov - **Issues described below**
  - time-b.timefreq.bldrdoc.gov - **Issues described below**
  - time-c.timefreq.bldrdoc.gov - **Issues described below**
  - utcnist.colorado.edu - **Issues described below**
  - ntps1-2.uni-erlangen.de - **REFUSED ANY CONNECTION**
  - time.ien.it - **ALWAYS REPLIED CORRECTLY**
  - ptbtime2.ptb.de - **UDP: never replied, didnt refuse. TCP: never allowed connection, didnt refuse. They both timed out**

### UDP
**Behaviour exclusively with the US servers**
- After succesive request, the server will reply a near to zero string, making the time display as Jan 1st 1900
- Eventually after even more succesive requests, the server will not reply

### TCP
**Behaviour exclusively with the US servers**
- Sometimes when running TCP, we get an error "struct.error: unpack requires a buffer of 4 bytes". This is due to the server sending us an empty message after multiple succesive requests
- After succesive request, the server will reply a near to zero string, making the time display as Jan 1st 1900

## Server mode
- The server will listen for connections on port 37. When a connection is established, the client shall send an empty packet (UDP), or open a connection (TCP) to which our server will return the 32-bit number (time) and close the connection.
