import socket
import struct

HOST = '127.0.0.1'
PORT = 2912

def recv_full(sock, n):
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data


def receive_message(sock):
    raw_length = recv_full(sock, 4)
    if not raw_length:
        return None

    length = struct.unpack('!I', raw_length)[0]
    data = recv_full(sock, length)

    return data.decode('utf-8')

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

            response = receive_message(client)
            print(f"[AI] {response}" )
    except:
        print("unexcepted error")
    finally:
        client.close()


if __name__ == "__main__":
    start_client()