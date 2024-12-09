import socket
import threading
import signal
import sys
import time

# List to keep track of connected clients
clients = []

# Broadcast messages to all clients
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)

# Handle communication with a single client
def handle_client(client_socket):
    while True:
        try:
            # Receive message from the client
            message = client_socket.recv(1024)
            if not message:
                break
            broadcast(message, client_socket)
        except:
            break
    
    # Remove client from the list and close the connection
    clients.remove(client_socket)
    client_socket.close()

# Function to stop the server
def stop_server(server_socket):
    print("\nNo clients connected. Shutting down the server...")
    for client in clients:
        client.close()
    server_socket.close()
    sys.exit(0)

# Timer function to shut down after 30 seconds if no clients connect
def start_shutdown_timer(server_socket, start_time):
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time >= 30 and len(clients) == 0:
            stop_server(server_socket)
        time.sleep(1)

# Main function to set up the server
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('25.2.47.86', 2620))  # Binding to all available IP addresses on port 5555
    server.listen(5)
    print("Server is listening for connections...")

    # Get the server start time
    start_time = time.time()

    # Start a separate thread to monitor the shutdown timer
    shutdown_thread = threading.Thread(target=start_shutdown_timer, args=(server, start_time))
    shutdown_thread.daemon = True
    shutdown_thread.start()

    while True:
        try:
            client_socket, client_address = server.accept()
            print(f"Connection from {client_address} established.")
            clients.append(client_socket)

            # Reset the timer because a client has connected
            start_time = time.time()

            # Start a new thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(client_socket,))
            client_thread.start()

        except Exception as e:
            print(f"Error accepting connection: {e}")
            break

if __name__ == "__main__":
    start_server()
