import socket


ClientSocket = socket.socket()
host = '127.0.0.1'
port = 4097

print('Waiting for connection')
try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))


while True:
    input_string = input("Enter a list of elements separated by space [first: data, second: process, third: event "
                         "no., fourth: model no.]:")
    userList = input_string.split()
    data = [int(i) for i in userList]
    Cmd = b"".join(int.to_bytes(d, length=2, byteorder='little', signed=False) for d in data)

    ClientSocket.send(Cmd)
    Response = ClientSocket.recv(6)
    print(Response)
