import socket
import threading
import tkinter as tk
import sys

# Define constants for the client
HOST = 'localhost'
PORT = 8000

global receive_thread
global stop_thread

root = tk.Tk()

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((HOST, PORT))

# Function to handle incoming messages
def receive_messages():
    while True:
        try:
            if stop_thread == True:
                sys.exit(0)
                break
            # Receive data from the server
            data = client_socket.recv(1024)
            if not data:
                break

            # Update the chat window with the received message
            chat_window.insert(tk.END, data.decode() + '\n', ('server', 'received'))
            # Move the scrollbar to the bottom
            chat_window.yview(tk.END)
        except:
            client_socket.close()
            break

# Function to send messages to the server
def send_message(event=None):
    # Get the message from the input field
    message = input_field.get()

    # Clear the input field
    input_field.delete(0, tk.END)

    # Send the message to the server
    client_socket.send(message.encode())

    # Insert the message into the chat window
    chat_window.insert(tk.END, f"{message}\n", ('user', 'sent'))
    # Move the scrollbar to the bottom
    chat_window.yview(tk.END)

# Function to kill threads exit event
def on_closing():
    client_socket.close()
    # stop_thread = True
    # print("Closed Pressed and currently Closing")
    sys.exit(0)
    # receive_thread.set()

# Create the GUI
root.title("Chat Client")

# Create the chat window and online clients frame
chat_frame = tk.Frame(root)
chat_frame.pack(side=tk.TOP, padx=10, pady=10)

online_clients_frame = tk.Frame(chat_frame)
online_clients_frame.pack(side=tk.RIGHT, padx=10)

scrollbar = tk.Scrollbar(chat_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

chat_window = tk.Text(chat_frame, height=20, width=50,
                      yscrollcommand=scrollbar.set)
chat_window.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

# coming_chat_msgs = tk.Text(chat_frame, height=20, width=50,yscrollcommand=scrollbar.set)
# coming_chat_msgs.pack(side=tk.RIGHT, padx=10, pady=10)

scrollbar.config(command=chat_window.yview)

# Define the message tags
chat_window.tag_config('user', foreground='blue')
chat_window.tag_config('server', foreground='green')
chat_window.tag_configure("sent", justify="right")
chat_window.tag_configure("received", justify="left")

root.option_add("*Font", "TkFixedFont")
root.option_add("*sent.Font", "TkFixedFont")
root.option_add("*received.Font", "TkFixedFont")


# Create the input field and send button
input_frame = tk.Frame(root)
input_frame.pack(side=tk.BOTTOM, padx=10, pady=10)

input_field = tk.Entry(input_frame, width=40)
input_field.bind("<Return>", send_message)
input_field.pack(side=tk.LEFT)

send_button = tk.Button(input_frame, text="Send", command=send_message)
send_button.pack(side=tk.LEFT)

# Create the list of online clients
online_clients_label = tk.Label(online_clients_frame, text="Online Clients:")
online_clients_label.pack(side=tk.TOP)

online_clients_listbox = tk.Listbox(online_clients_frame, height=20, width=20)
online_clients_listbox.pack(side=tk.BOTTOM, padx=10, pady=10)


# Function to update the list of online clients
def update_online_clients(online_clients):
    # Clear the current list of online clients
    online_clients_listbox.delete(0, tk.END)

    # Add each online client to the listbox
    for client in online_clients:
        online_clients_listbox.insert(tk.END, client)


# update_online_clients(['ahmad', 'mohammad'])


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


# Create a new thread to handle incoming messages
stop_thread = False
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Start the main loop
tk.mainloop()