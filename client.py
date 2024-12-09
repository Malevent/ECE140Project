import socket
import threading
import tkinter as tk
from tkinter import simpledialog, scrolledtext

# Function to receive messages from the server and update the chat window
def receive_messages(client_socket, chat_window):
    while True:
        try:
            # Receive a message from the server
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                # Prepend the sender's name to the received message
                chat_window.config(state=tk.NORMAL)  # Make it editable temporarily
                
                # Split the message into name and message parts
                sender, msg = message.split(":", 1)

                # Insert the sender's name with the appropriate color
                if sender == "You":
                    chat_window.insert(tk.END, f"{sender}: ", 'you')
                else:
                    chat_window.insert(tk.END, f"{sender}: ", 'other_user')

                # Insert the message with no color (black)
                chat_window.insert(tk.END, f"{msg}\n")
                
                chat_window.yview(tk.END)  # Auto-scroll to the bottom
                chat_window.config(state=tk.DISABLED)  # Make it read-only again
        except:
            chat_window.config(state=tk.NORMAL)
            chat_window.insert(tk.END, "Connection to server lost.\n")
            chat_window.config(state=tk.DISABLED)
            break

# Function to send messages to the server and display locally
def send_message(client_socket, message_entry, chat_window, username):
    message = message_entry.get()
    if message:
        # Display the sent message locally in the chat window with the username
        chat_window.config(state=tk.NORMAL)  # Make chat window editable temporarily
        chat_window.insert(tk.END, f"You: ", 'you')  # Display with blue color for name
        chat_window.insert(tk.END, f"{message}\n")  # Display message in black text
        chat_window.yview(tk.END)  # Auto-scroll to the bottom
        chat_window.config(state=tk.DISABLED)  # Make chat window read-only again

        # Send the message to the server, including the username
        client_socket.send(f"{username}: {message}".encode('utf-8'))
        message_entry.delete(0, tk.END)  # Clear the input field

# Function to set up the chat window after connecting to the server
def open_chat_window(client_socket, username):
    # Set up the main window for chatting
    root = tk.Tk()
    root.title("Chat Client")

    # Create a ScrolledText widget for the chat window
    chat_window = scrolledtext.ScrolledText(root, width=50, height=20, wrap=tk.WORD)
    chat_window.pack(padx=10, pady=10)
    chat_window.config(state=tk.DISABLED)  # Make chat window read-only initially

    # Create an entry widget for typing messages
    message_entry = tk.Entry(root, width=40)
    message_entry.pack(padx=10, pady=5)

    # Create a button to send messages
    send_button = tk.Button(root, text="Send", width=10, command=lambda: send_message(client_socket, message_entry, chat_window, username))
    send_button.pack(pady=5)

    # Configure tags for different colors
    chat_window.tag_configure('you', foreground='blue')  # Blue for "You" (name only)
    chat_window.tag_configure('other_user', foreground='red')  # Red for other users' names

    # Start a thread to listen for incoming messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, chat_window))
    receive_thread.daemon = True  # Allows the thread to exit when the main program exits
    receive_thread.start()

    # Start the Tkinter event loop for the chat window
    root.mainloop()

# Function to ask the user for their name after connecting to the server
def get_username():
    username = simpledialog.askstring("Enter your name", "Please enter your name:")
    if username:
        return username
    else:
        return "Anonymous"  # Default name if the user doesn't enter anything

# Function to attempt to connect to the server and open the chat window
def connect_to_server(ip_address):
    server_port = 5555
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((ip_address, server_port))
        print(f"Connected to server at {ip_address}.")

        # Ask for the username after connection
        username = get_username()

        # Open the chat window after successful connection
        open_chat_window(client, username)

    except Exception as e:
        print(f"Error connecting to server: {e}")

# Function to create the initial window where the user enters the server IP address
def start_initial_window():
    initial_window = tk.Tk()
    initial_window.title("Enter Server IP Address")

    # Label for the IP entry prompt
    ip_label = tk.Label(initial_window, text="Enter the server IP address:")
    ip_label.pack(padx=10, pady=10)

    # Entry widget for the IP address
    ip_entry = tk.Entry(initial_window, width=30)
    ip_entry.pack(padx=10, pady=10)

    # Function to handle the connect button click
    def on_connect_button_click():
        ip_address = ip_entry.get()
        if ip_address:
            initial_window.destroy()  # Close the IP entry window
            connect_to_server(ip_address)  # Try to connect to the server

    # Button to connect to the server
    connect_button = tk.Button(initial_window, text="Connect", command=on_connect_button_click)
    connect_button.pack(pady=20)

    # Start the Tkinter event loop for the initial window
    initial_window.mainloop()

if __name__ == "__main__":
    start_initial_window()
