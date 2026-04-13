import socket
import threading

HOST = '127.0.0.1'
PORT = 2912

# Обработчик клиента
def handle_client(conn, addr):
    print(f"[CONNECTION] {addr} connected")

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            message = data.decode('utf-8')
            print(f"[{addr}] -> {message}")

            conn.sendall(message.lower().encode('utf-8'))

    except Exception as e:
        print(f"[ERROR] {addr}: {e}")

    finally:
        conn.close()
        print(f"[CONNECTION] {addr} disconected")


# Запуск сервера
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[SERVER START] {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()

        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        print(f"[CONNECTION COUNT] {threading.active_count() - 1}")


if __name__ == "__main__":
    start_server()