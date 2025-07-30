import socket
def send_variable(ip, port, value):
    with socket.create_connection((ip, port)) as sock:
        sock.sendall(('SET:' + str(value)).encode())
        response = sock.recv(1024).decode()
        print("Ответ сервера:", response)

# Запрос IP сервера у пользователя
server_ip = input("Введите IP сервера: ")
server_port = 11012
encoding=input('ключ шефрования: ')
while True:
    a = input()
    c = ''
    for x in a:
        for y in range(len(encoding)):
            if x == encoding[y]:
                c+=str(y)+' '
    send_variable(server_ip, server_port, c)