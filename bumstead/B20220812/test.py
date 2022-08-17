import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_socket.bind(('localhost', 12345))
server_socket.listen(0)

client_socket, addr = server_socket.accept()
data = client_socket.recv(65535)

print(data.decode())

client_socket.send(data)