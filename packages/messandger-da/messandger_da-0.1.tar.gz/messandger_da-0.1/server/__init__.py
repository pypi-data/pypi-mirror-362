import socket
import threading

# Глобальные переменные
server_variable = None
server_running = True

def handle_client(conn, addr):
    global server_variable
    try:
        data = conn.recv(1024).decode()
        if not data:
            return
        if data.startswith('SET'):
            # Обновление переменной
            new_value = data[len('SET:'): ]
            server_variable = new_value
            conn.send('OK'.encode())
        elif data == 'GET':
            # Отправка текущего значения
            if server_variable is None:
                server_variable = '0'  # Значение по умолчанию
            conn.send(('V' + str(server_variable)).encode())
        else:
            conn.send('Unknown command'.encode())
    finally:
        conn.close()

def start_server():
    global server_running
    host = '0.0.0.0'
    port = 11012
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f'Server started at {host}:{port}')
        while server_running:
            try:
                conn, addr = s.accept()
                threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
            except:
                break
        print('Server stopped.')

def stop_server():
    global server_running
    server_running = False
    # Триггер для разрыва accept
    try:
        with socket.create_connection(('localhost', 12345), timeout=1):
            pass
    except:
        pass

if __name__ == "__main__":
    start_server()