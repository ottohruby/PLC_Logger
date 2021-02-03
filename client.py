import socket

ClientSocket = socket.socket()
host = '10.54.2.225'
port = 4200

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

#Response = ClientSocket.recv(1024)
while True:
    Input = input('Say Something: ')
    ClientSocket.send(str.encode(Input))
    Response = ClientSocket.recv(512)
    print(Response)

ClientSocket.close()
