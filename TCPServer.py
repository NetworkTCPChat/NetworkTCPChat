import socket
import threading
from helpers.color_helper import colors, colored
#from munch import Munch

# Define constants for the server
HOST = 'localhost'
PORT = 45863
MAX_CLIENTS = 5

# Create a dictionary to hold all connected clients and their usernames
connected_clients = {}

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(MAX_CLIENTS)




# Function to handle incoming client connections
def handle_client(client_socket, client_address):
    # Prompt the client for their username
    username = client_socket.recv(1024).decode().strip()

    # Add the client to the dictionary of connected clients
    connected_clients[client_socket] = {'username' : username}

    color = client_socket.recv(1024).decode().strip()
    
    if color not in colors: color = 'normal'
    
    # Add the client to the dictionary of connected clients
    connected_clients[client_socket]['color'] = color
    
    # Send a welcome message to the client
    client_socket.send(f"Welcome to the chat room, {username}!\r\n".encode())

    # Print client address in server's terminal
    print("Client Connected: " + str(client_address))
    
    for c in connected_clients.keys():
        if c != client_socket:
            temp = f"""\r\n<<<========  {connected_clients[client_socket]['username']} has just joined the room  ========>>>\r\n"""
            c.send(
                temp.encode())

    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(1024).decode()
            if not data:
                break
            
            if data.startswith('\color_'):
                new_color = data.split('_')[1]
                old_color = connected_clients[client_socket]['color']
                connected_clients[client_socket]['color'] = new_color if new_color in colors else old_color
                continue
            
            # Broadcast the message to all connected clients
            for c in connected_clients.keys():
                if c != client_socket:
                    msg = f"{connected_clients[client_socket]['username']}: {data}"
                    co = connected_clients[client_socket]['color']
                    colored_msg = colored(msg, co)
                    c.send(colored_msg.encode())
        except:
            # Remove the client from the dictionary of connected clients
            del connected_clients[client_socket]
            client_socket.close()
            break


# Function to handle client requests for the list of connected clients
def list_clients(client_socket):
    client_list = ""
    for c in connected_clients.values():
        client_list += c['username'] + "\n"
    if client_list == "":
        client_list = "No other clients connected\n"
    client_socket.send(client_list.encode())


# Main loop to handle incoming connections
while True:
    # Accept incoming connections
    client_socket, client_address = server_socket.accept()

    # Create a new thread to handle client requests for the list of connected clients
    list_thread = threading.Thread(target=list_clients, args=(client_socket,))
    list_thread.start()

    # Create a new thread to handle the client connection
    client_thread = threading.Thread(
        target=handle_client, args=(client_socket, client_address))
    client_thread.start()
