import socket
import re
from _thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

IP_address = '127.0.0.1'

Port = 4711

server.bind((IP_address, Port))

# limiting to 100 connections max.
server.listen(100)

list_of_clients = []


def client_thread(connection, addr) -> None:
    """
    Function handles the communication with client and runs on single thread per client.
    :return: None
    """
    connection.send("Hello, welcome to the chat-server version: 1".encode('utf-8'))
    connection.send(
        "Usage: Please enter the NICK <nick>, then start sending messages using MSG <text>".encode('utf-8'))

    while True:
        message = connection.recv(2048)
        if not message:
            print("Connection might be broken, Removing connection: {}...".format(connection))
            remove(connection)
            break
        else:
            nick_name = ''
            message_string = message.decode("utf-8")
            if re.search('NICK (.*)', message_string, re.IGNORECASE):
                nick_name = re.search('NICK (.*)', message_string, re.IGNORECASE).group(1)
                if 0 < len(nick_name) <= 12 and re.match("^[A-Za-z0-9\_]+$", nick_name):
                    message_to_send = 'MSG: Welcome ' + nick_name
                    send_message_to_connection(message_to_send.encode("utf-8"), connection)
                    # valid client, so client can communicate further with server
                    print("{} is registered successfully with server, can start sending messages..."
                          .format(nick_name))
                    communicate_with_client(connection, nick_name)
                else:
                    message_to_send = 'ERR: Nick name should be less than 12 characters and allowed characters ' \
                                      'are upper case, lower case, number and _. Client sent: ' + nick_name
                    send_message_to_connection(message_to_send.encode("utf-8"), connection)
            else:
                message_to_send = 'ERR: Nick name should start with command NICK <text>'
                send_message_to_connection(message_to_send.encode("utf-8"), connection)


def communicate_with_client(connection, nick_name) -> None:
    """
    Sends the given message to client.
    :return: None
    """
    while True:
        message = connection.recv(2048)
        if not message:
            print("no message received from client, connection might be broken")
            remove(connection)
            break
        else:
            client_message = message.decode('utf-8')
            if re.search('MSG', client_message, re.IGNORECASE):
                client_message = re.search('MSG (.*)', client_message, re.IGNORECASE).group(1)
                if 0 < len(client_message) > 255 and re.match("^[^\x00-\x7F]*$", client_message) is None:
                    message_to_send = "ERR: {} Message should be less than 255 characters".format(nick_name)
                else:
                    message_to_send = "MSG: {} {}".format(nick_name, client_message)
            else:
                message_to_send = "ERR: should be in format of MSG <text>"
            connection.send(message_to_send.encode("utf-8"))


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
                print("Exception occurred while sending message to {}, removing the client".format(connection))
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
    print("Welcome to the chat server...")
    while True:
        conn, addr = server.accept()

        # Maintains a list of clients
        list_of_clients.append(conn)

        # prints the address of the user that just connected
        print(addr[0] + " client connected")

        # creates and assigns thread for every client
        start_new_thread(client_thread, (conn, addr))

    server.close()


if __name__ == '__main__':
    main()
