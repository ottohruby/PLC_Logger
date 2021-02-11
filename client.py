import socket

ClientSocket = socket.socket()
host = '10.54.2.225'
port = 4097

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

#Response = ClientSocket.recv(1024)
while True:
    Input = input('Say Something: ')
    ClientSocket.send(int.to_bytes(int(Input), length=12, byteorder='little', signed=False))
    Response = ClientSocket.recv(12)
    print(Response)

ClientSocket.close()
