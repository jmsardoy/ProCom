#!/usr/bin/env python

import socket

TCP_IP   = '127.0.0.1'
TCP_PORT = 5005

BUFFER_SIZE = 1024

print '------------------------------------'
print 'Write->  Exit  <-to close the session'
print '------------------------------------'
print 'Ip: ',TCP_IP
print '------------------------------------'
print 'Port: ',TCP_PORT
print '------------------------------------'

##################################
## Inicializacion del socket
##################################
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, int(TCP_PORT)))
#s.settimeout(None)


print '------------------------------------'
init_message = s.recv(BUFFER_SIZE)
print '------------------------------------'
print init_message
print '------------------------------------'
user = raw_input('Introduce User: ')
s.send(user)
response = s.recv(BUFFER_SIZE)
if response !='OK':
    print '------------------------------------'
    print 'User Not Allowed'
    print '------------------------------------'

    s.close()
    exit()

print '------------------------------------'
print 'Connected'
print '------------------------------------'


while True:
    ## Envio el mensaje
    MESSAGE = raw_input('ToSend: ')
    s.send(MESSAGE)
    data = s.recv(BUFFER_SIZE)
    print "Echo: ", data
    if MESSAGE=='Exit':
        print 'Close Session'
        break

s.close()

