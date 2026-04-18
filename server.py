import socket
import threading
import requests
import json
import os
import struct
from datetime import datetime
from dotenv import load_dotenv
import sqlite3


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
    , timeout=1000)
    response_json = response.json()

    try:
        if response.status_code == 200:
            return response_json['choices'][0]['message']['content']
        else:
            print("----------------------JSON---------------")
            print(response_json)
            print("----------------------JSON---------------")
            return f"ERROR {response.status_code}"
    except:
        print(response_json)
        return "ERROR"

def send_message(conn, text):
    data = text.encode('utf-8')
    length = struct.pack('!I', len(data))  # 4 байта длины
    conn.sendall(length + data)

def handle_client(openrouterApiKey, conn, addr):
    print(f"[CONNECTION] {addr} connected")
    connect = sqlite3.connect("chat.db")
    cursor = connect.cursor()

    try:
        
        while True:
            data = conn.recv(1024)
            if not data:
                break

            message = data.decode('utf-8')
            print(f"[{addr}] -> Client: {message}")
            response = sendAiChat(openrouterApiKey, message)
            print(f"[{addr}] -> Ai: {response}")

            send_message(conn, response)
            cursor.execute(
            "INSERT INTO messages (user_text, ai_text, remoteIp, created_at) VALUES (?, ?, ?, ?)",
            (message, response, str(addr), datetime.now().isoformat())
            )

    except Exception as e:
        print(f"[ERROR] {addr}: {e}")

    finally:
        connect.commit()
        conn.close()
        connect.close()
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