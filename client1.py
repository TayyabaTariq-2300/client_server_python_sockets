# === CLIENT ===
import socket
import sounddevice as sd
import numpy as np
import threading

CHUNK_DURATION = 0.02
RATE = 48000
CHUNK = int(RATE * CHUNK_DURATION)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', 0))  # Bind to any available port

server_ip = '127.0.0.1'  # Use your actual server IP in LAN testing
server_port = 5000

def send_audio():
    def callback(indata, frames, time, status):
        if status:
            print("Input error:", status)
        try:
            sock.sendto(indata.tobytes(), (server_ip, server_port))
        except Exception as e:
            print("Error sending:", e)

    with sd.InputStream(samplerate=RATE, channels=1, dtype='float32',
                        callback=callback, blocksize=CHUNK):
        print("Mic streaming started...")
        while True:
            sd.sleep(1000)

def receive_audio():
    with sd.OutputStream(samplerate=RATE, channels=1, dtype='float32',
                         blocksize=CHUNK) as stream:
        print("Speaker playback started...")
        while True:
            try:
                data, _ = sock.recvfrom(4096)
                audio = np.frombuffer(data, dtype='float32')
                stream.write(audio)
            except Exception as e:
                print("Receive error:", e)

# Start both send and receive
threading.Thread(target=send_audio).start()
threading.Thread(target=receive_audio).start()
