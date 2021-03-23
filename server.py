#python3
import socket
import time
from config import *
import threading
import logging
#Initialization of logging into log file
logging.basicConfig(filename='sys_log/'+GetDate("file")+'.log', encoding = 'utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s')

def ParsePLCResponse(aData):
    # read and split data from client
    # first: error no., second: model, third: process no.
    errorNo = int.from_bytes(aData[0:2], byteorder='little', signed=False)
    processNo = int.from_bytes(aData[2:4], byteorder='little', signed=False)
    modelNo = int.from_bytes(aData[4:6], byteorder='little', signed=False)
    #print(f"Parsed data- ErrorNo: {errorNo}; ProcessNo: {processNo}; ModelNo: {modelNo}")
    return errorNo,processNo,modelNo


class ThreadedServer():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.ServerSocket = socket.socket()

        try:
            #self.ServerSocket(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.ServerSocket.bind((host, port))
            logging.info("Socket was binded %s",port)
        except socket.error as e:
            logging.error(e,exc_info=True)
            print(str(e))

    def listen(self):
        print('Waiting for a Connection..')
        logging.info("Waiting for connection")
        self.ServerSocket.listen(5)
        while True:
            try:
                client, address = self.ServerSocket.accept()
                print(f"Connected to: {address[0]}:{address[1]}")
                threading.Thread(target=self.listenClient, args=(client,)).start()
                logging.info("New connection added %s",client)
                print(f"Number active of threads: {threading.active_count()}")
                print(f"List of threads: {threading.enumerate()}")
            except socket.error as e:
                print(str(e))
                time.sleep(2)
                logging.error(e, exc_info=True)
        self.ServerSocket.close()

    def listenClient(self, connection):
        while True:
            try:
                data = connection.recv(6)
                logging.info("Received data: %s Lenght of data: %s",data,len(data))
            except socket.error as e:
                logging.info("Could not received data from PLC, given data %s",data)
                logging.error(e, exc_info=True)
                print("Could not receive data from PLC")
                break
            #print(f"Received data: {data}")
            
            try:
                data_parsed = ParsePLCResponse(data)  # words to tuple (ErrorNo,ProcessNo,ModelNo)
                LineOfLog = CreateRow(Get_Err(data_parsed[0],data_parsed[1]))
                WriteRow(LineOfLog, data_parsed[1])
                process = Get_Machine_From_Process(data_parsed[1])
                print (str(process)+" had error: "+LineOfLog)
            except Exception as e:
                logging.info('Something happned in Config.py')
                logging.error(e, exc_info=True)
                print(e)
                time.sleep(0.1)

            reply = int.to_bytes(123, length=6, byteorder='little', signed=False)  # debug
            if not data:
                logging.info("Data was not correct, check data!")
                logging.debug("Given data:%s",data)
                break
            #print(f"Server response: {reply}")
            connection.send(reply)
            logging.info("Reply from server to PLC was %s",reply)   
        connection.close()
        logging.debug("Connection was closed")


if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT = 4097

    server = ThreadedServer(HOST,PORT)
    server.listen()



