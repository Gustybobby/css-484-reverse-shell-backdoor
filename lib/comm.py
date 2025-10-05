import socket
import json
from . import logger


def send(sock: socket.socket, data, verbose: bool):
    jsondata = json.dumps(data)
    sock.send(jsondata.encode())
    logger.debug(f"[comm:send] {data}", verbose)


def receive(sock: socket.socket, verbose: bool):
    data = ""
    error = ""

    count = 0
    while count < 5:
        try:
            data = data + sock.recv(1024).decode().rstrip()
            logger.debug(f"[comm:receive] {data}", verbose)
            return json.loads(data)
        except ValueError as e:
            logger.debug(f"[comm:receive] error: {e}", verbose)
            error = e
        count += 1

    raise ValueError(f"[comm:receive] error: {error}")
