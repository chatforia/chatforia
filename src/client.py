import socket
import threading
from tkinter.constants import *
from constants import *
import tkinter as tk
from tkinter import scrolledtext
from tkinter.messagebox import *
from tkinter import filedialog as fd
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def save_chat():
    file = fd.asksaveasfilename(defaultextension="*.txt",
                                filetypes=(("Text Documents", "*.txt"), ("All files", "*.*")))

    with open(file, "w") as f:
        f.write(chatarea.get(1.0, END))


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.sendall(send_length)
    client.sendall(message)


def listen_for_incoming_messages():
    thread = threading.Thread(target=recive_messages)
    thread.daemon = True
    thread.start()


def recive_messages():
    while True:
        message = client.recv(HEADER).decode(FORMAT)

        if message:
            message += '\n'

            chatarea.insert(END, message)
            chatarea.yview(END)


def Join(event=None):
    if NameValue.get() == "":
        showerror("Error", "Error: Your name is not valid")
    else:
        joinbutton['state'] = 'disabled'
        JoinMessage = "[alert]"+NameValue.get()+" has been joined"
        nameEntry['state'] = 'disabled'
        send(JoinMessage)


def Send(event=None):
    if Message.get() == "":
        showerror("Error", "Error: Your message is not valid")
    else:
        full_message = NameValue.get()+' : '+Message.get()
        send(full_message)

        Message.set("")
        sendbox.update()


if __name__ == "__main__":
    root = tk.Tk()

    root.title("Client window")
    root.geometry("800x800")

    # themes
    root.tk.call('source',  'lib\\Sun-Valley-ttk-theme\\sun-valley.tcl')
    root.tk.call('set_theme', 'dark')

    NameValue = tk.StringVar()
    Message = tk.StringVar()

    chatarea = scrolledtext.ScrolledText()
    chatarea.pack(side=TOP, fill=X)

    # making the chat area read only
    chatarea.bind("<Key>", lambda e: "break")

    # menus
    menu = tk.Menu(root)

    filemenu = tk.Menu(menu, tearoff=0)
    filemenu.add_command(label="Save Chat", command=save_chat)

    menu.add_cascade(menu=filemenu, label="File")

    Form = tk.Frame(root, relief=SUNKEN, borderwidth=6)
    Form.pack(side="bottom")

    nameEntry = tk.Entry(Form, textvariable=NameValue)

    nameEntry.grid(column=0, row=0)

    joinbutton = tk.Button(Form, text="Join the server",
                           command=Join, font="Arial 9", padx=20)

    joinbutton.grid(column=2, row=0)
    sendbox = tk.Entry(Form, textvariable=Message)
    sendbox.grid(column=0, row=1)
    sendbutton = tk.Button(Form, text="Send", command=Send, padx=20)
    sendbutton.grid(column=2, row=1)
    root.config(menu=menu)
    listen_for_incoming_messages()

    root.mainloop()
