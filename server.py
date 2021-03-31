import socketserver
# python3
import socket
import time
from config import *
import threading
import logging

# Initialization of logging into log fie
logging.basicConfig(filename='sys_log/'+GetDate("file")+'.log', level=logging.DEBUG, format='%(asctime)s %(message)s')


def ParsePLCResponse(aData):
    # read and split data from client
    # first: error no., second: process, third: model no.
    errorNo = int.from_bytes(aData[0:2], byteorder='little', signed=False)
    processNo = int.from_bytes(aData[2:4], byteorder='little', signed=False)
    modelNo = int.from_bytes(aData[4:6], byteorder='little', signed=False)
    #print(f"Parsed data- ErrorNo: {errorNo}; ProcessNo: {processNo}; ModelNo: {modelNo}")
    return errorNo, processNo, modelNo


def ProcessData(data):
    try:
        data_parsed = ParsePLCResponse(data)  # words to tuple (ErrorNo,ProcessNo,ModelNo)
        LineOfLog = CreateRow(Get_Err(data_parsed[0], data_parsed[1]))
        WriteRow(LineOfLog, data_parsed[1])
        process = Get_Machine_From_Process(data_parsed[1])
        print(str(process) + " had error: " + LineOfLog)
    except Exception as e:
        logging.info('Something happened in Config.py')
        logging.error(e, exc_info=True)
        print(e)
        time.sleep(0.1)


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def setup(self):
        print("New client connected: " + str(threading.current_thread()), end=' ')
        print(self.client_address)
        print("Active threads: " + str(threading.active_count()))

    def finish(self):
        print("Client disconnected: " + str(threading.current_thread()), end=' ')
        print(self.client_address)


    def handle(self):
        while True:
            data = self.request.recv(6)
            logging.info("Received data: %s Lenght of data: %s", data, len(data))
            print(self.client_address, end='- ')
            # process if data is correct
            if not data:
                logging.info("Data was not correct, check data!")
                logging.debug("Given data:%s", data)
            else:
                logging.debug("Received data are correct")
                ProcessData(data)

            # send a response
            reply = int.to_bytes(123, length=6, byteorder='little', signed=False)  # debug
            self.request.sendall(reply)
            logging.info("Reply from server to PLC was %s", reply)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "0.0.0.0", 4097

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    with server:
        print("Server started")
        server.serve_forever()

