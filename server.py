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

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        data = self.request.recv(6)
        logging.info("Received data: %s Lenght of data: %s", data, len(data))

        # process if it is correct
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



if __name__ == "__main__":
    HOST, PORT = "localhost", 4097

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()