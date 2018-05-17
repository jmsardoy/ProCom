#!/usr/bin/env python

import socket
import threading
import os
import time

from framed_socket import FramedSocket

##############################################
## Clase que para armar un servidor Ethernet
##############################################
class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        ## Definicion el tipo de protocolo (IPv4) y el tipo de socket
        self.sock = FramedSocket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

        ## Creo un archivo de logeo
        self.filep = open('logs_session.txt','w')
        self.filep.close()
        self.access_list = ['pepe', 'papa']

    ## Metodo escucha
    def listen(self):
        ## Longitud del buffer de escucha
        self.sock.listen(5)
        while True:
            ## Identifica al cliente e IP
            client, address = self.sock.accept()
            client.settimeout(None)

            ## Escribo el inicio de sesion

            ## Respondo al cliente
            size = 1024
            client.send("Init Session")
            user = client.recv(size)
            if user in self.access_list:
                client.send('OK')
                self.log_connection(client, user, True)
            else:
                client.send('FAIL')
                self.log_connection(client, user, False)
            ## Abro un hilo
            threading.Thread(target=self.listenToClient, 
                             args=(client,address, user)).start()


    ## Metodo de respuesta
    def listenToClient(self, client, address, user):
        size = 1024
        date = time.strftime("%d_%b_%Y-%H:%M:%S", time.gmtime()) 
        file_name = "%s_%s"%(user, date)

        while True:
            try:
                data = client.recv(size)
                if data:
                    self.log_communication(file_name, client, user, data,
                                           send=False)
                    response = data
                    client.send(response)
                    self.log_communication(file_name, client, user, response,
                                           send=True)
                else:
                    raise error('Client disconnected')

            except:
                self.log_disconnection(client, user)
                client.close()
                return False

    ## Metodo de escritudo por inicio de sesion
    def log_connection(self,client, user, allowed=True):
        self.filep = open('logs_session.txt','a')
        if allowed: allowed = 'ALLOWED'
        else: allowed = 'NOT ALLOWED'
        self.filep.write('%s\tOpen  -> '%\
                         (time.strftime("%d %b %Y - %H:%M:%S", 
                                        time.gmtime())) + 
                        '%s '%str(client) +
                        'User -> %s '%user + allowed + '\n')
        self.filep.close()

    def log_disconnection(self, client, user):
        self.filep = open('logs_session.txt','a')
        self.filep.write('%s\tClose -> '%\
                         time.strftime("%d %b %Y - %H:%M:%S", 
                                       time.gmtime()) + 
                        '%s '%str(client) +
                        'User -> %s\n'%user)
        self.filep.close()
        
    def log_communication(self, file_name, client, user, data, send):
        if send: direction = "SEND   "
        else: direction    = "RECEIVE"
        self.filep = open(file_name, 'a')
        self.filep.write('%s' % time.strftime("%d %b %Y - %H:%M:%S", 
                                             time.gmtime()) 
                         + '\t%s ->' % direction
                         + '%s '%str(client) 
                         + 'User -> %s'%user
                         + '-> Data: %s \n' % data)
        self.filep.close()


if __name__ == "__main__":
    port_num = 5005
    ThreadedServer('',port_num).listen()
