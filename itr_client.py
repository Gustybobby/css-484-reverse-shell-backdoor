import socket
from lib import client, config

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect_server(sock, (config.IP, config.ITR_PORT), client.shell, 5)
