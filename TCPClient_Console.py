import socket
import threading
from helpers.color_helper import colors

# Define constants for the client
HOST = "localhost"
PORT = 29842

color = "normal"

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((HOST, PORT))

# Function to handle incoming messages


def receive_messages():
    while True:
        try:
            # Receive data from the server
            data = client_socket.recv(1024).decode()
            if not data:
                break

            # Print the message to the console
            # print(data.decode(), colors[color])
            print("\r\n", data, colors[color], "\r\n")
        except:
            client_socket.close()
            break


# Create a new thread to handle incoming messages
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()


name = input("please enter your name: ")
client_socket.send(name.strip().encode())

color = input("please choose a color from {}:  ".format(list(colors.keys())))
if color not in colors:
    print("Not Valid Color, normal is default")
    color = "normal"
print(
    '\r\n\x1b[4mTo change the color later on type:\x1b[0m "\\color \x1b[3mthe_new_color\x1b[0m"'
)
client_socket.send(color.strip().encode())


while True:
    # Get input from the user
    message = input()

    if message.startswith("\color_"):
        new_color = message.split("_")[1]
        old_color = color
        color = new_color if new_color in colors else old_color
        print(colors[color])

    # Send the message to the server
    client_socket.send(message.encode())
