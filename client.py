import socket
import time

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 4097

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

#Response = ClientSocket.recv(1024)
while True:
    input_string = input("Enter a list of elements separated by space [iCommSen iData1Sen iData2Sen]:")
    userList = input_string.split()
    data = [int(i) for i in userList]
    Cmd = b"".join(int.to_bytes(d, length=2, byteorder='little', signed=False) for d in data)

    ClientSocket.send(Cmd)
    Response = ClientSocket.recv(6)
    print(Response)


