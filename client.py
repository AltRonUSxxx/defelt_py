import socket

HOST = '127.0.0.1'
PORT = 2912

def start_client():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        print(f"Connected to {HOST}:{PORT}")
    except:
        print("Couldn't connect to server")
        return

    try:
        while True:
            message = input()
            if message=="exit":
                break
            client.sendall(message.encode('utf-8'))

            response = client.recv(1024).decode('utf-8')
            print(f"[СЕРВЕР] -> {response}")
    except:
        print("unexcepted error")
    finally:
        client.close()


if __name__ == "__main__":
    start_client()