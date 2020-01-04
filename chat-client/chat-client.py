import socket
import select
import sys
from argparse import ArgumentParser
from zenlog import log

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

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((parser.parse_args().ip_address, parser.parse_args().port))
    client_socket.setblocking(True)

    # Stay connected with server until the server is down
    while True:
        # maintains a list of possible input streams
        sockets_list = [sys.stdin, client_socket]
        try:
            read_sockets, write_socket, error_socket = select.select(sockets_list, [], [])
        except ValueError as e:
            log.error("Server communication is down, shutting down client")
            client_socket.close()
            sys.exit(1)
        for sockets in read_sockets:
            if sockets is not None:
                if sockets == client_socket:
                    message = sockets.recv(2048)
                    if not message:
                        client_socket.close()
                    log.info("-----------------------------------------")
                    log.info("Server Response: {}\n".format(message.decode("utf-8")))
                    log.info("-----------------------------------------")
                else:
                    message = input()
                    log.info("Sending message to server.... {}".format(message))
                    client_socket.send(message.encode('utf-8'))

    client_socket.close()


if __name__ == '__main__':
    main()
