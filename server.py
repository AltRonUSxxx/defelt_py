import socket
import threading
import requests
import json
import os
from dotenv import load_dotenv


HOST = '127.0.0.1'
PORT = 2912


def sendAiChat(openrouterApiKey, message):
    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {openrouterApiKey}",
    },
    data=json.dumps({
        "model": "openrouter/elephant-alpha",
        "messages": [
        {
            "role": "user",
            "content": message
        }
        ]
    })
    ).json()
    return response['choices'][0]['message']['content']


def handle_client(openrouterApiKey, conn, addr):
    print(f"[CONNECTION] {addr} connected")

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            message = data.decode('utf-8')
            print(f"[{addr}] -> Client: {message}")
            response = sendAiChat(openrouterApiKey, message)
            print(f"[{addr}] -> Ai: {response}")

            conn.sendall(response.encode('utf-8'))

    except Exception as e:
        print(f"[ERROR] {addr}: {e}")

    finally:
        conn.close()
        print(f"[CONNECTION] {addr} disconected")


def start_server():
    load_dotenv()
    openrouterApiKey= os.getenv('openrouterApiKey')
    if openrouterApiKey:
        print("openrouterApiKey has loaded")
    else:
        print("ERROR: openrouterApiKey not found")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    print(f"[SERVER START] {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()

        thread = threading.Thread(target=handle_client, args=(openrouterApiKey, conn, addr))
        thread.start()

        print(f"[CONNECTION COUNT] {threading.active_count() - 1}")


if __name__ == "__main__":
    start_server()