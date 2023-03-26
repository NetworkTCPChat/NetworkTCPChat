import socket
import threading
import tkinter as tk

# Define constants for the client
HOST = 'localhost'
PORT = 8000

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((HOST, PORT))

# Function to handle incoming messages


def receive_messages():
    while True:
        try:
            # Receive data from the server
            data = client_socket.recv(1024)
            if not data:
                break

            # Update the chat window with the received message
            chat_window.insert(tk.END, data.decode() + '\n', 'server')
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
    chat_window.insert(tk.END, f"You: {message}\n", 'user')
    # Move the scrollbar to the bottom
    chat_window.yview(tk.END)


# Create the GUI
root = tk.Tk()
root.title("Chat Client")

# Create the chat window
chat_frame = tk.Frame(root)
chat_frame.pack(side=tk.TOP, padx=10, pady=10)

scrollbar = tk.Scrollbar(chat_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

chat_window = tk.Text(chat_frame, height=20, width=50,
                      yscrollcommand=scrollbar.set)
chat_window.pack(side=tk.LEFT, padx=10, pady=10)

scrollbar.config(command=chat_window.yview)

# Define the message tags
chat_window.tag_config('user', foreground='blue')
chat_window.tag_config('server', foreground='green')

# Create the input field and send button
input_frame = tk.Frame(root)
input_frame.pack(side=tk.BOTTOM, padx=10, pady=10)

input_field = tk.Entry(input_frame, width=40)
input_field.bind("<Return>", send_message)
input_field.pack(side=tk.LEFT)

send_button = tk.Button(input_frame, text="Send", command=send_message)
send_button.pack(side=tk.LEFT)

# Create a new thread to handle incoming messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

# Start the main loop
tk.mainloop()
