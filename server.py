
#python3
import socket
import time
from config import *
import threading

def ParsePLCResponse(aData):
    # read and split data from client
    # first: error no., second: model, third: process no.
    errorNo = int.from_bytes(aData[0:2], byteorder='little', signed=False)
    processNo = int.from_bytes(aData[2:4], byteorder='little', signed=False)
    modelNo = int.from_bytes(aData[4:6], byteorder='little', signed=False)
    print(f"Parsed data- ErrorNo: {errorNo}; ProcessNo: {processNo}; ModelNo: {modelNo}")
    return errorNo,processNo,modelNo


class ThreadedServer():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.ServerSocket = socket.socket()

        try:
            self.ServerSocket.bind((host, port))
            print('Listening at port:',port)
        except socket.error as e:
            print(str(e))

    def listen(self):
        print('Waiting for a Connection..')
        self.ServerSocket.listen(5)
        while True:
            try:
                client, address = self.ServerSocket.accept()
                print(f"Connected to: {address[0]}:{address[1]}")
                threading.Thread(target=self.listenClient, args=(client,)).start()
                print(f"Number active of threads: {threading.active_count()}")
            except socket.error as e:
                print(str(e))
                time.sleep(2)
        self.ServerSocket.close()

    def listenClient(self, connection):
        while True:
            try:
                data = connection.recv(12)
            except socket.error:
                print("Could not receive data from PLC")
                break

            print(f"Received data: {data}")
            data_parsed = ParsePLCResponse(data)  # words to tuple (ErrorNo,ProcessNo,ModelNo)

            try:
                LineOfLog = CreateRow(Get_Err(data_parsed[0]))
                WriteRow(LineOfLog)
            except Exception as e:
                print(e)
                time.sleep(0.1)

            reply = int.to_bytes(123, length=6, byteorder='little', signed=False)  # debug
            if not data:
                break
            print(f"Server response: {reply}")
            connection.send(reply)
        connection.close()


if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT = 4200

    ThreadedServer(HOST,PORT).listen()



