import socket
import threading

HOST = '127.0.0.1'
PORT = 1234
LISTENER_LIMIT = 5
active_clients = []  # List of all currently connected users
lock = threading.Lock()  # Lock for thread safety

# Function to listen for upcoming messages from a client
def listen_for_messages(client, username):
    while True:
        try:
            message = client.recv(2048).decode('utf-8')
            if message:
                final_msg = f"{username}~{message}"
                send_messages_to_all(final_msg)
            else:
                print(f"The message sent from client {username} is empty")
                break
        except Exception as e:
            print(f"Error listening for messages from {username}: {e}")
            break

# Function to send message to a single client
def send_message_to_client(client, message):
    try:
        client.sendall(message.encode())
    except Exception as e:
        print(f"Error sending message to client: {e}")

# Function to send any new message to all the clients that
# are currently connected to this server
def send_messages_to_all(message):
    with lock:
        for user in active_clients:
            send_message_to_client(user[1], message)

# Function to handle client
def client_handler(client):
    try:
        # Server will listen for client message that will
        # Contain the username
        while True:
            username = client.recv(2048).decode('utf-8')
            if username:
                with lock:
                    active_clients.append((username, client))
                prompt_message = f"SERVER~{username} added to the chat"
                send_messages_to_all(prompt_message)
                break
            else:
                print("Client username is empty")
    except Exception as e:
        print(f"Error handling client: {e}")

    threading.Thread(target=listen_for_messages, args=(client, username)).start()

# Main function
def main():
    # Creating the socket class object
    # AF_INET: we are going to use IPv4 addresses
    # SOCK_STREAM: we are using TCP packets for communication
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Creating a try catch block
    try:
        # Provide the server with an address in the form of
        # host IP and port
        server.bind((HOST, PORT))
        print(f"Running the server on {HOST} {PORT}")
    except Exception as e:
        print(f"Unable to bind to host {HOST} and port {PORT}: {e}")
        return

    # Set server limit
    server.listen(LISTENER_LIMIT)

    try:
        # This while loop will keep listening to client connections
        while True:
            client, address = server.accept()
            print(f"Successfully connected to client {address[0]} {address[1]}")

            threading.Thread(target=client_handler, args=(client,)).start()
    except KeyboardInterrupt:
        print("Server shutting down.")
    finally:
        server.close()

if __name__ == '__main__':
    main()
