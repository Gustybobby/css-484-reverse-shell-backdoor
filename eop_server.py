from lib import config, eop_npp as eop, server


def open_eop_server():
    client, _ = server.open_server((config.IP, config.EOP_PORT))
    eop.script(client)


if __name__ == "__main__":
    open_eop_server()
