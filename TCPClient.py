import socket
import threading
import tkinter as tk

import sys
import textwrap
from datetime import datetime


global receive_thread
global stop_thread

# Define constants for the client
HOST = 'localhost'
PORT = 8000

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Function to handle incoming messages
usernames_set = set()

client_socket.connect((HOST, PORT))

root = tk.Tk()
root.configure(bg="#2E3440")
root.title('Chat')
def receive_messages():
    while True:
        try:
            if stop_thread == True:
                sys.exit(0)
                break

            data = client_socket.recv(1024).decode()
            
            if not data:
                break

            msg_type = data[0]
            msg = data[1:]

            if msg_type == 'o':
                if msg in usernames_set:
                    add_message(f"{msg} has just left the room", 'system')
                    usernames_set.remove(msg)
                else:
                    add_message(f"{msg} has just joined the room", 'system')
                    usernames_set.add(msg)
                update_online_clients(usernames_set)
            elif msg_type == 'O':
                curr_online_users = msg.split(',')
                curr_online_users.sort()
                root.title(f'Chat - {curr_online_users.__getitem__(curr_online_users.__len__()-1)}') 
                usernames_set.update(curr_online_users)
                update_online_clients(curr_online_users)
            elif msg_type in ['z', 'w']:
                add_message(msg, 'system')
            else:
                add_message(msg, 'others')
        except:
            client_socket.close()
            break


def send_message(event=None):
    message = input_field.get()
    input_field.delete(0, tk.END)
    client_socket.send(message.encode())
    add_message(message, 'me')


def on_closing():
    client_socket.close()
    sys.exit(0)


chat_frame = tk.Frame(root)
chat_frame.pack(side=tk.TOP, padx=10, pady=10)
chat_frame.configure(bg="#2E3440")

online_clients_frame = tk.Frame(chat_frame)
online_clients_frame.pack(side=tk.RIGHT, padx=10)
online_clients_frame.configure(bg="#2E3440")

scrollbar = tk.Scrollbar(chat_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

chat_window = tk.Text(chat_frame, height=20, width=50,
                      yscrollcommand=scrollbar.set, wrap="word")
chat_window.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

scrollbar.config(command=chat_window.yview)

chat_window.tag_config('user', foreground='#88C0D0')
chat_window.tag_config('server', foreground='#8FBCBB')
chat_window.tag_config('small', font=("Helvetica", 7))
chat_window.tag_config('greycolour', foreground="#D8DEE9")
chat_window.tag_config("me", justify="right")
chat_window.tag_config("others", justify="left")
chat_window.tag_config("system", justify="center")
chat_window.tag_config("right", justify="right")
chat_window.tag_config("small", font=("Helvetica", 7))
chat_window.tag_config("colour", foreground="#D8DEE9")

chat_window.config(state=tk.DISABLED)

chat_window.configure(background='black')

root.option_add("*Font", "TkFixedFont")
root.option_add("*sent.Font", "TkFixedFont")
root.option_add("*received.Font", "TkFixedFont")

input_frame = tk.Frame(root)
input_frame.pack(side=tk.BOTTOM, padx=10, pady=10)
input_frame.configure(bg="#2E3440")

input_field = tk.Entry(input_frame, width=40)
input_field.bind("<Return>", send_message)
input_field.pack(side=tk.LEFT)

send_button = tk.Button(input_frame, text="Send", command=send_message)
send_button.pack(side=tk.LEFT)
send_button.configure(bg="#D8DEE9", fg="#2E3440")

online_clients_label = tk.Label(online_clients_frame, text="Online Clients:")
online_clients_label.pack(side=tk.TOP)
online_clients_label.configure(bg="#2E3440", fg="#D8DEE9")

online_clients_listbox = tk.Listbox(online_clients_frame, height=20, width=20)
online_clients_listbox.pack(side=tk.BOTTOM, padx=10, pady=10)

online_clients_listbox.configure(bg="#4C566A", fg="#D8DEE9", highlightbackground="#81A1C1",
                                 highlightcolor="#81A1C1", selectbackground="#81A1C1", selectforeground="#D8DEE9")


def get_time_formatted():
    return datetime.now().strftime("%a %I-%M %p \n")


def add_message(msg, sender):
    
    chat_window.config(state=tk.NORMAL)

    fa = "#13f252"
    bg_color = "black"
    text_position = ""
    tags = ""
    text_direction = tk.LEFT

    match sender:
        case 'others':
            text_position = "left"
            fa = "#13f252"
            tags = 'others'
        case 'system':
            text_position = "center"
            fa = "#ffffff"
            tags = 'system'
            text_direction = tk.CENTER
        case 'me':
            text_position = "right"
            fa = "#fc541c"
            tags = 'me'
            
    
    chat_window.insert(tk.END, '\n ', text_position)
    chat_window.insert(tk.END, get_time_formatted(),('small', 'greycolour', text_position))
    chat_window.insert(tk.END, ' ', text_position)

    chat_window.config(state=tk.DISABLED)
    
    message = tk.Label(chat_window, fg=fa, text=msg, wraplength=200, font=("Arial", 10), bg=bg_color, bd=4, justify=text_direction, relief="flat", anchor="center")

    # chat_window.insert(tk.END, '\n ', 'center')
    # chat_window.window_create(tk.END, window=message)
    # chat_window.config(foreground="#0000CC", font=("Helvetica", 9))
    # chat_window.yview(tk.END)

    chat_window.window_create(tk.END, window=message)
    chat_window.insert(tk.END, '\n', "center")
    chat_window.tag_add(tags, "end-2l", "end-1c")
    chat_window.config(foreground="#0000CC", font=("Helvetica", 9))
    chat_window.yview(tk.END)



    


def send(msg, is_sent=False):
    chat_window.config(state=tk.NORMAL)
    # chat_window.insert(tk.END, get_time_formatted()+' ', ("small", "left", "greycolour"))
    chat_window.insert(tk.END, '\n ', "right")
    chat_window.window_create(tk.END, window=tk.Label(chat_window, fg="#000000", text=msg,
                                                      wraplength=200, font=("Arial", 10), bg="lightblue", bd=4, justify="left"))
    chat_window.insert(tk.END, '\n ', "left")
    chat_window.config(foreground="#0000CC", font=("Helvetica", 9))
    chat_window.yview(tk.END)

    

    # res = "Bot's response goes into here, elongating this message to test textwrap"
    # chat_window.insert(tk.END, get_time_formatted()+' ', ("small", "greycolour", "left"))
    # chat_window.window_create(tk.END, window=tk.Label(chat_window, fg="#000000", text=res,
    # wraplength=200, font=("Arial", 10), bg="#DDDDDD", bd=4, justify="left"))
    # chat_window.insert(tk.END, '\n ', "right")
    # chat_window.config(state=tk.DISABLED)
    # chat_window.yview(tk.END)

# send("Hello, World!")
# send("Hello, World!")


def on_listbox_double_click(event):
    # Get the selected item from the listbox
    selection = online_clients_listbox.get(
        online_clients_listbox.curselection())

    # Perform the desired action, e.g. print the selected item
    input_field.delete(0, tk.END)
    input_field.insert(tk.END, f"@{selection} ")
    input_field.focus_set()
    # print(selection)


online_clients_listbox.bind("<Double-Button-1>", on_listbox_double_click)


# Function to update the list of online clients
def update_online_clients(online_clients):
    # Clear the current list of online clients
    online_clients_listbox.delete(0, tk.END)

    # Add each online client to the listbox
    for client in online_clients:
        online_clients_listbox.insert(tk.END, client)


# Create a new thread to handle incoming messages
stop_thread = False
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the main loop
tk.mainloop()
