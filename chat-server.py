
# Python program to implement server side of chat room. 
import socket
import re
from _thread import *
import sys

"""The first argument AF_INET is the address domain of the 
socket. This is used when we have an Internet Domain with 
any two hosts The second argument is the type of socket. 
SOCK_STREAM means that data or characters are read in 
a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# checks whether sufficient arguments have been provided 


# takes the first argument from command prompt as IP address 
IP_address = '127.0.0.1'

# takes second argument from command prompt as port number 
Port = 2004

""" 
binds the server to an entered IP address and at the 
specified port number. 
The client must be aware of these parameters 
"""
server.bind((IP_address, Port))

""" 
listens for 100 active connections. This number can be 
increased as per convenience. 
"""
server.listen(100)

list_of_clients = []


def client_thread(connection, addr):
    # sends a message to the client whose user object is conn
    print(addr)
    connection.send("Hello, welcome to the chat-server version: 1 \n".encode('utf-8'))
    connection.send("Usage: Please enter the NICK <nick>, then start sending messages using MSG <text> \n".encode('utf-8'))

    while True:
        message_to_send = ''
        message = connection.recv(2048)
        if not message:
            """message may have no content if the connection 
                           is broken, in this case we remove the connection"""
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



def communicate_with_client(connection, nick_name):
    while True:
        message_to_send = ''
        message = connection.recv(2048)
        if not message:
            """message may have no content if the connection 
                       is broken, in this case we remove the connection"""
            print("removing connection after nick")
            remove(connection)
            break
        else:
            client_message = message.decode('utf-8')
            if len(client_message) > 255:
                print("ERR " + client_message)
            else:
                print("Success")



"""Using the below function, we broadcast the message to all 
clients who's object is not the same as the one sending 
the message """
def send_message_to_connection(message, connection):
    for clients in list_of_clients:
        if clients == connection:
            try:
                connection.send(message)
            except Exception as e:
                connection.close()

                # if the link is broken, we remove the client
                remove(clients)


"""The following function simply removes the object 
from the list that was created at the beginning of  
the program"""


def remove(connection):
    if connection in list_of_clients:
        list_of_clients.remove(connection)


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