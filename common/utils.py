import socket


def get_random_port():
    sock = socket.socket()
    sock.bind(('', 0))
    return sock.getsockname()[1]
