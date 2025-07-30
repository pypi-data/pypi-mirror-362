import socket
def send_variable(ip, port, value):
    with socket.create_connection((ip, port)) as sock:
        sock.sendall(('SET:' + str(value)).encode())
        response = sock.recv(1024).decode()
        print("Ответ сервера:", response)

# Запрос IP сервера у пользователя
server_ip = input("Введите IP сервера: ")
server_port = 12345
print('запускает файл (имя.расширение|содержание,)')
while True:
    a = input()
    send_variable(server_ip, server_port, a)