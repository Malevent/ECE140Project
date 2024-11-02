import socket # import socket to use in client function

def client_side_using_TCP():
    server_address = ("localhost", 65432) # assume localhost for now. Probably will change to a vm ip. Use designated port 65432.

    # now define a TCP/IP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock: # shorthand alternative to try catch statement
        sock.connect(server_address) # connect to server addr

        try:
            # send msg to serv
            while (1):
                message_input = input("Enter message to send (or exit to quit):")

                #exit inf loop if user types "exit".
                if (message_input.lower() == "exit"): # convert input to all lowercase and check if equals exit
                    print("Terminating the connection.")
                    break
                else:
                    sock.sendall(message_input.encode())

                    #look for server response
                    response = sock.recv(1024) # specify max amount of data client can receive at a time in byte data
                    print("Received message:", response.decode())
        finally:
            #terminate/close socket
            print("Closing the socket")
            sock.close()

# main method to call function
client_side_using_TCP()
