#!/usr/bin/env python
# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Revisión 2014 Carlos Bederián
# Revisión 2011 Nicolás Wolovick
# Copyright 2008-2010 Natalia Bidart y Daniel Moisset
# $Id: server.py 656 2013-03-18 23:49:11Z bc $


import errno
import optparse
import socket
import sys
from os.path import exists
import threading
import connection
from constants import *

class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket,directory):

        threading.Thread.__init__(self)
        self.socket = clientsocket
        self.directory = directory
        print ("New connection added: ", clientAddress)
    def run(self):
        try:
            con = connection.Connection(self.socket, self.directory)
            con.handle()
            self.socket.close()
        except IOError as e:
            if e.errno == errno.EPIPE:
                con.close()

class Server(object):
    """
    El servidor, que crea y atiende el socket en la dirección y puerto
    especificados donde se reciben nuevas conexiones de clientes.
    """

    def __init__(self, addr=DEFAULT_ADDR, port=DEFAULT_PORT,
                 directory=DEFAULT_DIR):
        print("Serving %s on %s:%s." % (directory, addr, port))
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((addr, port))
        print ("socket binded to %s" %(port)) 
        self.directory = directory

    def serve(self):
        """
        Loop principal del servidor. Se acepta una conexión a la vez
        y se espera a que concluya antes de seguir.
        """
        try:        
            print ("socket is listening")  
            while True:
                self.socket.listen(1)
                clientsock, addr = self.socket.accept()
                newthread = ClientThread(addr, clientsock,self.directory)
                newthread.start()

        except KeyboardInterrupt:
            print("KeyboardInterrupt. Closing connection")
            self.socket.close()


def main():
    """Parsea los argumentos y lanza el server"""

    parser = optparse.OptionParser()
    parser.add_option(
        "-p", "--port",
        help="Número de puerto TCP donde escuchar", default=DEFAULT_PORT)
    parser.add_option(
        "-a", "--address",
        help="Dirección donde escuchar", default=DEFAULT_ADDR)
    parser.add_option(
        "-d", "--datadir",
        help="Directorio compartido", default=DEFAULT_DIR)

    options, args = parser.parse_args()
    if len(args) > 0:
        parser.print_help()
        sys.exit(1)
    try:
        port = int(options.port)
    except ValueError:
        sys.stderr.write(
            "Numero de puerto invalido: %s\n" % repr(options.port))
        parser.print_help()
        sys.exit(1)

    server = Server(options.address, port, options.datadir)
    server.serve()


if __name__ == '__main__':
    main()
