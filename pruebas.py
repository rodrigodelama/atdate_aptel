import sys
import time
import socket
my_time = time.gmtime(0)
my_act_time = time.gmtime(time.time())
print(my_time[0])
print(my_act_time)

a = socket.getaddrinfo('time-a.timefreq.bldrdoc.gov',37)[0][-1]
print(a)

'''
argv_str = " "
argv_str.join(sys.argv[index] for index in sys.argv)
print(argv_str)


argv_str = argv_str.join(str(index) for index in sys.argv)
print("argv_str: ", argv_str)
'''