# encoding: utf-8
# Revisión 2019 (a Python 3 y base64): Pablo Ventura
# Copyright 2014 Carlos Bederián
# $Id: connection.py 455 2011-05-01 00:32:09Z carlos $

import socket
from base64 import b64encode
from os import listdir, mkdir
from os.path import dirname, exists, getsize, isfile, join, relpath

from constants import *


class Connection(object):
    """
    Conexión punto a punto entre el servidor y un cliente.
    Se encarga de satisfacer los pedidos del cliente hasta
    que termina la conexión.
    """
    def __init__(self, new_socket_conn, directory):
        self.socket = new_socket_conn
        self.directory = directory
        self.closed = False
        self.status = 0

    def handle(self):
        """
        Atiende eventos de la conexión hasta que termina.
        """
        try:
            queue = ''
            while not self.closed:
                data = self.socket.recv(1024).decode('ascii')
                if data:
                    queue += data
                    queue = self.process_queue(queue)
                else:
                    print('No data received. Closing connection.')
                    self.closed = True
        except(socket.error, socket.gaierror):
            self.status = INTERNAL_ERROR
            self.socket.send((str(self.status) + ' ' + error_messages[self.status] + EOL).encode())

    def process_queue(self, queue):
        while EOL in queue and not self.closed:
            (line, queue) = queue.split(EOL, 1)
            if '\n' in line:
                self.status = BAD_EOL
                response = ''
            else:
                response = self.commands(line)
            self.socket.send((str(self.status) + ' ' + error_messages[self.status] + EOL).encode() + response.encode())
        return queue

    def commands(self, line):
        args = line.split()
        if not args:
            self.status = INVALID_COMMAND
            return ''

        command = args[0]
        response = ''
        if command == 'quit':
            if len(args) != 1:
                self.status = INVALID_ARGUMENTS
            else:
                response = self.quit()
        elif command == 'get_file_listing':
            if len(args) != 1:
                self.status = INVALID_ARGUMENTS
            else:
                response = self.get_file_listing()
        elif command == 'get_metadata':
            if len(args) != 2:
                self.status = INVALID_ARGUMENTS
            else:
                response = self.get_metadata(args[1])
        elif command == 'get_slice':
            if len(args) != 4:
                self.status = INVALID_ARGUMENTS
            elif not (args[2].isdigit() and args[3].isdigit()):
                self.status = INVALID_ARGUMENTS
            else:
                response = self.get_slice(args[1], int(args[2]), int(args[3]))
        else:
            self.status = INVALID_COMMAND
        return response

    def get_file_listing(self):
        if not exists(self.directory):
            mkdir(self.directory)
        files = listdir(self.directory)
        files = [f for f in files if isfile(join(self.directory, f))]
        self.status = CODE_OK
        return EOL.join(files + [EOL])

    def get_metadata(self, filename):
        if not self.is_valid_filename(filename):
            return ''
        path = self.directory + '/' + filename
        filesize = str(getsize(path))
        self.status = CODE_OK
        return filesize + EOL

    def get_slice(self, filename, offset, size):
        if not self.is_valid_filename(filename):
            return ''
        if not (offset >= 0 and size >= 0):
            self.status = INVALID_ARGUMENTS
            return ''
        path = self.directory + '/' + filename
        filesize = getsize(path)
        if (offset + size) > filesize:
            self.status = BAD_OFFSET
            return ''
        with open(path, 'rb') as file_data:
            file_data.seek(offset)
            buff = bytearray()
            read_left = size
            while read_left > 0:
                to_read = min(1024, size)
                data = file_data.read(to_read)
                buff.extend(data)
                read_left -= to_read
        self.status = CODE_OK
        buff = b64encode(buff)
        return buff.decode('ascii') + EOL

    def quit(self):
        self.status = CODE_OK
        self.closed = True
        return ''

    def is_valid_filename(self, filename):
        if len(filename) > 80:
            self.status = FILE_NOT_FOUND
            return False
        for char in filename:
            if not char in VALID_CHARS:
                self.status = BAD_REQUEST
                return False
        path = self.directory + '/' + filename
        if not isfile(path):
            self.status = FILE_NOT_FOUND
            return False
        return True
