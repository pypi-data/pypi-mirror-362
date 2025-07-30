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
server_port = 11012
encoding=input('ключ дешифрования: ')
a=get_variable(server_ip, server_port)
while True:
    b=get_variable(server_ip, server_port)
    if b != a:
        a=b
        c=''
        b=b.split(' ')
        for i in b[:-1]:
            c+=encoding[int(i)]
        print(c)