import socket
import threading
from tkinter.constants import *
from constants import *
import tkinter as tk
from tkinter import scrolledtext
from tkinter.messagebox import *
from tkinter import filedialog as fd
from tkinter import ttk
from PIL import ImageTk, Image
import sys

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# it loads resources and thread to start the application


def loading():
    global logoimage
    logoimage = Image.open("img\\favicon.ico")
    logoimage = ImageTk.PhotoImage(logoimage)


def setting():
    settingwindow = tk.Toplevel()

    Checkcolor = tk.IntVar(settingwindow)
    CheckVisible = tk.IntVar(settingwindow)

    def save():
        if Checkcolor.get() == 0:
            chatarea.config(fg="white")
        elif Checkcolor.get() == 1:
            chatarea.config(fg="blue")

        if CheckVisible.get() == 0:
            for i in range(0, 3):
                menu.entryconfigure(i, state=tk.NORMAL)
        elif CheckVisible.get() == 1:
            for i in range(0, 3):
                menu.entryconfigure(i, state=tk.DISABLED)
    settingwindow.geometry("300x300+0+0")

    tab = ttk.Notebook(settingwindow)

    editorsettings = ttk.Frame(settingwindow)
    menusettings = ttk.Frame(settingwindow)

    # editors setting
    colorcheckbox = ttk.Checkbutton(
        editorsettings, text="Apply a Blue color", variable=Checkcolor, onvalue=1, offvalue=0)

    # menu setting
    menucheckbox = ttk.Checkbutton(
        menusettings, text="Disable menu bar", variable=CheckVisible, onvalue=1, offvalue=0)

    tab.add(editorsettings, text="Editor")
    tab.add(menusettings, text="Menu")

    SaveButton = ttk.Button(settingwindow, text="Save",
                            style="Accent.TButton", command=save)

    tab.pack()
    colorcheckbox.pack()
    menucheckbox.pack()
    SaveButton.pack()
    settingwindow.mainloop()


def Set_Light_theme():
    root.tk.call("set_theme", "light")
    menu.tk.call("set_theme", "light")


def Set_Dark_theme():
    root.tk.call("set_theme", "dark")
    menu.tk.call("set_theme", "dark")


def save_chat():
    try:
        file = fd.asksaveasfilename(defaultextension="*.txt",
                                    filetypes=(("Text Documents", "*.txt"), ("All files", "*.*")))

        with open(file, "w") as f:
            f.write(chatarea.get(1.0, END))

    except FileNotFoundError:
        print("Great")


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


def on_close(event=None):
    message = askyesno("Do you want to leave", "Leave, yes or not?")
    if message:
        send(f"!DISC {NameValue.get()}")
        sys.exit()
    else:
        pass


if __name__ == "__main__":
    # function to load the application

    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", on_close)
    loading()
    root.iconphoto(False, logoimage)
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

    theme = tk.Menu(menu, tearoff=0)
    theme.add_command(label="light", command=Set_Light_theme)
    theme.add_command(label="dark", command=Set_Dark_theme)

    properties = tk.Menu(menu, tearoff=0)
    properties.add_command(label="settings", command=setting)

    menu.add_cascade(menu=filemenu, label="File")
    menu.add_cascade(menu=theme, label="Theme")
    menu.add_cascade(menu=properties, label="Properties")

    Form = ttk.Frame(root, relief=SUNKEN, borderwidth=6)
    Form.pack(side="bottom")

    nameEntry = tk.Entry(Form, textvariable=NameValue)

    nameEntry.grid(column=0, row=0)

    joinbutton = ttk.Button(Form, text="Join the server",
                            command=Join,  style="Accent.TButton")
    sendbox = tk.Entry(Form, textvariable=Message)
    sendbutton = ttk.Button(Form, text="Send", command=Send,
                            style="Accent.TButton")

    sendbox.grid(column=0, row=1)
    joinbutton.grid(column=2, row=0, padx=10, pady=5)
    sendbutton.grid(column=2, row=1, padx=10, pady=5)
    root.config(menu=menu)
    listen_for_incoming_messages()
    root.mainloop()
