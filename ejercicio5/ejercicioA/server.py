#!/usr/bin/env python

import socket
import threading
import os
import time

##############################################
## Clase que para armar un servidor Ethernet
##############################################
class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        ## Definicion el tipo de protocolo (IPv4) y el tipo de socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
            user = client.recv(size)
            if user in self.access_list:
                client.send('OK')
                self.loadDic(client, user, True)
            else:
                client.send('FAIL')
                self.loadDic(client, user, False)
            ## Abro un hilo
            threading.Thread(target = self.listenToClient,args = (client,address, user)).start()


    ## Metodo de respuesta
    def listenToClient(self, client, address, user):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    response = data
                    client.send(response)
                else:
                    raise error('Client disconnected')

            except:
                self.filep = open('logs_session.txt','a')
                self.filep.write('%s\tClose -> '%\
                                 time.strftime("%d %b %Y - %H:%M:%S", 
                                               time.gmtime()) + 
                                '%s '%str(client) +
                                'User -> %s\n'%user)
                self.filep.close()

                client.close()
                return False

    ## Metodo de escritudo por inicio de sesion
    def loadDic(self,clientN, user, allowed=True):
        self.filep = open('logs_session.txt','a')
        if allowed: allowed = 'ALLOWED'
        else: allowed = 'NOT ALLOWED'
        self.filep.write('%s\tOpen  -> '%\
                         (time.strftime("%d %b %Y - %H:%M:%S", 
                                        time.gmtime())) + 
                        '%s '%str(clientN) +
                        'User -> %s '%user + allowed + '\n')
        self.filep.close()


if __name__ == "__main__":
    port_num = 5005
    ThreadedServer('',port_num).listen()
