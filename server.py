#python3
import socket
import os
import time
import csv
from _thread import *
from config import *

ServerSocket = socket.socket()
host = '0.0.0.0'
port = 61000
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection..')
ServerSocket.listen(5)

def threaded_client(connection):
    #connection.send(str.encode('Welcome to the Server\n'))
    while True:
        data = connection.recv(512)
        LineOfLog = CreateRow(Get_Err(data))
        WriteRow(LineOfLog)
        time.sleep(0.1)
        #read and split data from client
        #first: error no., second: model, third: process no.
        reply = 'Server Says: ' + data.decode('utf-8')
        if not data:
            break
        connection.send(str.encode(reply))
    connection.close()
#
#def write_log(process,data):

while True:
    try:
        Client, address = ServerSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(threaded_client, (Client, ))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
    except socket.error as e:
        print(str(e))
        time.sleep(2)

ServerSocket.close()
