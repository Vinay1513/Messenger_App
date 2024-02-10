import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, messagebox

HOST = '127.0.0.1'
PORT = 1234

BACKGROUND_COLOR = '#2C2C2C'
TEXT_COLOR = 'white'
BUTTON_COLOR = '#219653'
BUTTON_HOVER_COLOR = '#1E8449'
BUTTON_ACTIVE_COLOR = 'purple'
BUTTON_TEXT_COLOR = 'black'
ENTRY_COLOR = '#333333'
FONT = ("Helvetica", 17)
BUTTON_FONT = ("Helvetica", 15)
SMALL_FONT = ("Helvetica", 13)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def add_message(message):
    message_box.config(state=tk.NORMAL)
    message_box.insert(tk.END, message + '\n')
    message_box.config(state=tk.DISABLED)
    message_box.yview(tk.END)

def on_button_hover(event):
    username_button.config(bg=BUTTON_HOVER_COLOR)

def on_button_leave(event):
    username_button.config(bg=BUTTON_COLOR)

def connect():
    try:
        client.connect((HOST, PORT))
        add_message("[SERVER] Successfully connected to the server")
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")

    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")

    threading.Thread(target=listen_for_messages_from_server, args=(client,)).start()

    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)

def send_message():
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
        message_textbox.delete(0, tk.END)
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")

root = tk.Tk()
root.geometry("600x600")
root.title("My Messenger")
root.resizable(False, False)
root.config(bg=BACKGROUND_COLOR)

root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=4)
root.grid_rowconfigure(2, weight=1)

top_frame = tk.Frame(root, width=600, height=100, bg=BACKGROUND_COLOR)
top_frame.grid(row=0, column=0, sticky=tk.NSEW)

middle_frame = tk.Frame(root, width=600, height=400, bg=BACKGROUND_COLOR)
middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

bottom_frame = tk.Frame(root, width=600, height=100, bg=BACKGROUND_COLOR)
bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

username_label = tk.Label(top_frame, text="Enter username:", font=FONT, bg=BACKGROUND_COLOR, fg=TEXT_COLOR)
username_label.pack(side=tk.LEFT, padx=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=ENTRY_COLOR, fg=TEXT_COLOR, width=23)
username_textbox.pack(side=tk.LEFT)

username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, command=connect)
username_button.pack(side=tk.LEFT, padx=15)

message_textbox = tk.Entry(bottom_frame, font=FONT, bg=ENTRY_COLOR, fg=TEXT_COLOR, width=38)
message_textbox.pack(side=tk.LEFT, padx=10)

message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=BUTTON_COLOR, fg=BUTTON_TEXT_COLOR, command=send_message)
message_button.pack(side=tk.LEFT, padx=10)

message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=ENTRY_COLOR, fg=TEXT_COLOR, width=67, height=26.5)
message_box.config(state=tk.DISABLED)
message_box.pack(side=tk.TOP)

username_button.bind("<Enter>", on_button_hover)
username_button.bind("<Leave>", on_button_leave)

def listen_for_messages_from_server(client):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message != '':
                username = message.split("~")[0]
                content = message.split('~')[1]
                add_message(f"[{username}] {content}")
            else:
                messagebox.showerror("Error", "Message received from client is empty")
        except Exception as e:
            print(f"Error listening for messages from server: {e}")
            break

root.mainloop()



def listen_for_messages_from_server(client):

    while 1:

        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split("~")[0]
            content = message.split('~')[1]

            add_message(f"[{username}] {content}")
            
        else:
            messagebox.showerror("Error", "Message recevied from client is empty")

# main function
def main():

    root.mainloop()
    
if __name__ == '__main__':
    main()