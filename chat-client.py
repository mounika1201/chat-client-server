import socket
import select
import sys
from argparse import ArgumentParser
from zenlog import log

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def main() -> None:
    """
    Entry point of this module
    :return: None
    """
    parser = ArgumentParser()
    parser.add_argument('--ip-address', '-ip', nargs='?', default='127.0.0.0', type=str,
                        help='pass --ip-address or -ip to use the server ip address')

    parser.add_argument('--port', '-p', nargs='?', default='2000', type=int,
                        help='pass --port or -p for passing the server port to the script')

    client_socket.connect((parser.parse_args().ip_address, parser.parse_args().port))
    client_socket.setblocking(True)

    # Stay connected with server until the server is down
    while True:
        # maintains a list of possible input streams
        sockets_list = [sys.stdin, client_socket]

        """ There are two possible input situations. Either the 
        user wants to give  manual input to send to other people, 
        or the server is sending a message  to be printed on the 
        screen. Select returns from sockets_list, the stream that 
        is reader for input. So for example, if the server wants 
        to send a message, then the if condition will hold true 
        below.If the user wants to send a message, the else 
        condition will evaluate as true"""
        try:
            read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
        except ValueError as e:
            log.error("Server communication is down, shutting down client")
            client_socket.close()
            sys.exit(1)
        for socks in read_sockets:
            if socks is not None:
                if socks == client_socket:
                    message = socks.recv(2048)
                    if not message:
                        client_socket.close()
                    log.info("Server Message: " + str(message))
                else:
                    message = input("Please enter the message for server")
                    client_socket.send(message.encode('utf-8'))
    client_socket.close()


if __name__ == '__main__':
    main()
