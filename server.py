import socket
import time
import logger
import threading
import logging
import os
from pathlib import Path
from utils import *

HOST = '0.0.0.0'
PORT = 49901


class ThreadedServer(object):
    def __init__(self, host, port):
        """
        Init server

        :param host: IP address of server
        :param port: Port number of server
        """

        self.host = host
        self.port = port
        self.ServerSocket = socket.socket()

        # Bind the socket
        try:
            self.ServerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.ServerSocket.bind((host, port))
            logging.info(f"Socket was bound {port}")
        except socket.error as e:
            logging.error(e, exc_info=True)
            print(str(e))

    def listen(self):
        """
        This function listens for new clients.
        If a new client is found then a new thread is started.
        The new thread calls listenClient function.

        :return: None
        """

        print('Waiting for a Connection..')
        logging.info("Waiting for connection")
        self.ServerSocket.listen(5)
        while True:
            try:
                client, address = self.ServerSocket.accept()
                print(f"Connected to: {address[0]}:{address[1]}")
                threading.Thread(target=self.listen_to_client, args=(client,)).start()
                logging.info(f"New connection added {client}")
                print(f"Number active of threads: {threading.active_count()}")
                print(f"List of threads: {threading.enumerate()}")
            except socket.error as e:
                print(str(e))
                time.sleep(2)
                logging.error(e, exc_info=True)

    def listen_to_client(self, connection):
        """
        This function runs for each connected client
        It serves to receive data, process data and send a response back to client

        :param connection: Client's socket
        :return: None
        """

        while True:
            data = None
            try:  # Receive data
                data = connection.recv(128)
                logging.info(f"Received data: {data}, Length of data: {len(data)}")
            except socket.error as e:
                logging.error(f"Could not receive data, given data {data}")
                logging.error(e, exc_info=True)
                print("Could not receive data")
                break

            logging.debug(f"Received data: {data}")

            if not data:  # No data received
                logging.error("Data were not received, check data!")
                logging.debug(f"Given data: {data}")
                break

            reply = int.to_bytes(123, length=6, byteorder='little', signed=False)
            try:  # Select which machine sent data and decode them
                if b'\r' in data:
                    # The robot sends \r delimiter and it must receive the same delimiter back at the end of the message
                    reply = b'OK\r'
                    data = binary_string_to_tuple(data, 4, '\r')
                else: # PLC
                    data = binary_bytes_to_tuple(data, 4)
            except Exception as e:
                logging.error("An unexpected error has happened in utils.py")
                logging.error(e, exc_info=True)

            try:  # Log received data
                info = logger.Info(data)
                logger.Logger(info)
            except logger.LoggerError:
                pass
            except Exception as e:
                logging.error('Unexpected error has happened in logger.py')
                logging.error(e, exc_info=True)
                print(e)
                time.sleep(0.1)

            connection.send(reply)
            logging.info(f"Reply from server to was {reply}")

        connection.close()
        logging.info("Connection was closed")


if __name__ == "__main__":
    # Create sys_log folder in script directory if it does not exists
    logger_dir = os.path.dirname(os.path.realpath(__file__)) + '/sys_log/'
    Path(logger_dir).mkdir(parents=True, exist_ok=True)
    # Initialization of logging
    logging.basicConfig(filename=logger_dir + get_date("file") + '.log', level=logging.DEBUG,
                        format='%(asctime)s %(message)s')

    server = ThreadedServer(HOST, PORT)
    server.listen()
