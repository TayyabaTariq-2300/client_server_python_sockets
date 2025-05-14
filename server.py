



# === SERVER ===
import socket
import threading

CHUNK_DURATION = 0.02
RATE = 48000
CHUNK = int(RATE * CHUNK_DURATION)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    sock.bind(('0.0.0.0', 5000))
    print("Server bound to 0.0.0.0:5000")
except socket.error as e:
    print(f"Error binding socket: {e}")
    exit(1)

clients = []

def receive_and_forward():
    while True:
        try:
            data, addr = sock.recvfrom(4096)
            if addr not in clients:
                clients.append(addr)

            for client in clients:
                if client != addr:
                    sock.sendto(data, client)
        except Exception as e:
            print(f"Error: {e}")

receive_and_forward()
