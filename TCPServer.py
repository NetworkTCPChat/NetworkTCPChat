import socket
import threading

# Define constants for the server
HOST = 'localhost'
PORT = 8000
MAX_CLIENTS = 5

# Create a dictionary to hold all connected clients and their usernames
connected_clients = {}
username_to_socket = {}
usernames_set = set()

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(MAX_CLIENTS)


# Function to handle incoming client connections
def handle_client(client_socket, client_address):
    try:
        # Prompt the client for their username
        client_socket.send(b"\nPlease enter your username: ")
        username = client_socket.recv(1024).decode().strip()
        while username in usernames_set:
            client_socket.send(
                b"\nThis username is already taken, please choose another one: ")
            username = client_socket.recv(1024).decode().strip()

        # Add the client to the dictionary of connected clients
        connected_clients[client_socket] = username
        username_to_socket[username] = client_socket
        usernames_set.add(username)

        # Send a welcome message to the client
        client_socket.send(f"Welcome to the chat room, {username}!\n".encode())

        for c in connected_clients.keys():
            if c != client_socket:
                c.send(
                    f"{connected_clients[client_socket]} has just joined the room".encode())

        while True:
            try:
                # Receive data from the client
                data = client_socket.recv(1024).decode()

                if not data:
                    break

                if data.startswith("@"):
                    splitted = data.split(' ')
                    curr_username = splitted[0]
                    curr_username = curr_username[1:]
                    if curr_username in usernames_set:
                        message = ' '.join(splitted[1:])
                        username_to_socket[curr_username].send(
                            f"{connected_clients[client_socket]}: {message}".encode())
                else:
                    # Broadcast the message to all connected clients
                    for c in connected_clients.keys():
                        if c != client_socket:
                            c.send(
                                f">>>>>{connected_clients[client_socket]}: {data}".encode())
            except Exception as e:
                print(e)
                # Remove the client from the dictionary of connected clients
                del connected_clients[client_socket]
                del username_to_socket[username]
                usernames_set.remove(username)
                
                client_socket.close()
                break
    except Exception as e:
        print(e)
        del connected_clients[client_socket]
        client_socket.close()
         


# Function to handle client requests for the list of connected clients
def list_clients(client_socket):
    client_list = ""
    for c in connected_clients.values():
        client_list += c + "\n"
    if client_list == "":
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