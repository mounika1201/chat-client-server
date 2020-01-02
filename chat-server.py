import socket
import re
from _thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# takes the first argument from command prompt as IP address 
IP_address = '127.0.0.1'

# takes second argument from command prompt as port number 
Port = 2004

server.bind((IP_address, Port))

# limiting to 100 connections max.
server.listen(100)

list_of_clients = []


def client_thread(connection, addr) -> None:
    """
    Function handles the communication with client and runs on single thread per client.
    :return: None
    """
    # sends a message to the client whose user object is conn
    print(addr)
    connection.send("Hello, welcome to the chat-server version: 1 \n".encode('utf-8'))
    connection.send(
        "Usage: Please enter the NICK <nick>, then start sending messages using MSG <text> \n".encode('utf-8'))

    while True:
        message_to_send = ''
        message = connection.recv(2048)
        if not message:
            print("removing connection before nick")

            remove(connection)
            raise RuntimeError
        else:

            message_string = message.decode("utf-8")
            if re.search('NICK', message_string, re.IGNORECASE):
                nick_name = re.search('NICK (.*)', message_string, re.IGNORECASE).group(1)
                if len(nick_name) <= 12 and re.match("^[A-Za-z0-9\_]+$", nick_name):
                    message_to_send = 'MSG: Welcome ' + nick_name
                else:
                    message_to_send = 'ERR: Nick name should be less than 12 characters and allowed characters ' \
                                      'are upper case, lower case, number and _. Client sent: ' + nick_name

            send_message_to_connection(message_to_send.encode("utf-8"), connection)

            communicate_with_client(connection, nick_name)


def communicate_with_client(connection, nick_name) -> None:
    """
    Sends the given message to client.
    :return: None
    """
    while True:
        message = connection.recv(2048)
        if not message:
            print("removing connection after nick")
            remove(connection)
            break
        else:
            client_message = message.decode('utf-8')
            if len(client_message) > 255:
                connection.send(
                    "ERR: {} Message should be less than 255 characters\n".format(nick_name).encode("utf-8"))
            else:
                connection.send("MSG: {} {}\n".format(nick_name, client_message).encode("utf-8"))


def send_message_to_connection(message, connection) -> None:
    """
    Sends the given message to the given connection.
    :return: None
    """
    for clients in list_of_clients:
        if clients == connection:
            try:
                connection.send(message)
            except Exception as e:
                connection.close()
                # Link might be broken, remove the connection
                remove(clients)


def remove(connection) -> None:
    """
    Function to remove the connection from list of connections.
    :return: None
    """
    if connection in list_of_clients:
        list_of_clients.remove(connection)


def main() -> None:
    """
    Entry point of this module
    :return: None
    """
    while True:
        """Accepts a connection request and stores two parameters,  
        conn which is a socket object for that user, and addr  
        which contains the IP address of the client that just  
        connected"""
        conn, addr = server.accept()

        """Maintains a list of clients for ease of broadcasting 
        a message to all available people in the chatroom"""
        print("starting appended")
        list_of_clients.append(conn)

        # prints the address of the user that just connected
        print(addr[0] + " connected")

        # creates and individual thread for every user
        # that connects
        start_new_thread(client_thread, (conn, addr))

    server.close()


if __name__ == '__main__':
    main()
