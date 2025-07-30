import socket

server_ip = input("Введите IP сервера: ")

def get_variable(ip, port):
    with socket.create_connection((ip, port)) as sock:
        sock.sendall('GET'.encode())
        data = sock.recv(1024).decode()
        if data.startswith('V'):
            return data[1:]
        return None
server_port = 12345
a='1.txt|я тут,'
while True:
    if str(get_variable(ip=server_ip, port=server_port)) == a:
        print('я тут')