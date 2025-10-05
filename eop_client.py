import socket
from lib import client, config


def connect_eop_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect_server(sock, (config.IP, config.EOP_PORT), client.shell, 5)
