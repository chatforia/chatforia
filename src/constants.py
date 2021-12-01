import socket
# import threading

HOST = socket.gethostbyname(socket.gethostname())
PORT = 8000
ADDR = (HOST, PORT)
FORMAT = 'utf-8'
HEADER = 64
DISC = "!DISC"
