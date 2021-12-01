import socket
import threading
from constants import *

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(ADDR)
clients = []


def handle_client(conn, addr):
    connected = True
    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISC:
                    connected = False
                print(f"{addr}{msg}")
                print("[Operation] sending to all clients")
                for sock in clients:
                    sock.send(msg.encode(FORMAT))

        except OSError:
            print(f"{addr} has been removed")
            clients.remove(conn)

    for sock in clients:
        sock.close()
    socket.close()


def start():
    socket.listen()
    while True:
        conn, addr = socket.accept()
        clients.append(conn)
        print(f"[Alert] {addr} has been Connected")
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print(F"ACTIVE: SERVER IS ON {ADDR}")
start()
