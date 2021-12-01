import socket
import threading
from tkinter.constants import *
from constants import *
import tkinter as tk
from tkinter import scrolledtext


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.sendall(send_length)
    client.sendall(message)


def listen_for_incoming_messages():
    thread = threading.Thread(target=recive_messages)
    thread.start()


def recive_messages():
    while True:
        message = client.recv(HEADER).decode(FORMAT)
        if message:
            message += '\n'
            
            chatarea.insert(END, message)
            chatarea.yview(END)


def Join():
    JoinMessage = "[alert]"+NameValue.get()+" has been joined"
    sendjoinmessage = JoinMessage.encode(FORMAT)
    msglength = len(sendjoinmessage)
    sendlength = str(msglength).encode(FORMAT)
    sendlength += b' ' * (HEADER-len(sendlength))
    client.send(sendlength)
    client.send(sendjoinmessage)



def Send():
    
    full_message = NameValue.get()+' : '+Message.get()
    send(full_message)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Client window")
    root.geometry("800x800")

    NameValue = tk.StringVar()
    Message = tk.StringVar()

    chatarea = scrolledtext.ScrolledText()
    chatarea.pack(side=TOP, fill=X)

    Form = tk.Frame(root, relief=SUNKEN, borderwidth=6)
    Form.pack(side="bottom")

    nameEntry = tk.Entry(Form, textvariable=NameValue)

    nameEntry.grid(column=0, row=0)

    joinbutton = tk.Button(Form, text="Join the server", command=Join)

    joinbutton.grid(column=2, row=0)
    sendbox = tk.Entry(Form, textvariable=Message)
    sendbox.grid(column=0, row=1)
    sendbutton = tk.Button(Form, text="Send", command=Send)
    sendbutton.grid(column=2, row=1)
    listen_for_incoming_messages()

    root.mainloop()