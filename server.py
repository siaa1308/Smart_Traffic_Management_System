import socket
import time

HOST = 'localhost'
PORT = 12345

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print("Server listening on port", PORT)

conn, addr = server_socket.accept()
print("Connected by", addr)

signal_color = "red"
last_change_time = time.time()

MIN_GREEN_DURATION = 3  # seconds
MIN_RED_DURATION = 5    # seconds

while True:
    data = conn.recv(1024)
    if not data:
        break

    try:
        vehicle_count, ambulance_present = map(int, data.decode().split(","))
    except:
        continue

    current_time = time.time()
    time_since_change = current_time - last_change_time

    if ambulance_present:
        if signal_color != "green":
            signal_color = "green"
            last_change_time = current_time

    elif signal_color == "green":
        if vehicle_count <= 10 and time_since_change >= MIN_GREEN_DURATION:
            signal_color = "red"
            last_change_time = current_time

    elif signal_color == "red":
        if vehicle_count > 10 and time_since_change >= MIN_RED_DURATION:
            signal_color = "green"
            last_change_time = current_time

    conn.sendall(signal_color.encode())

conn.close()
server_socket.close()