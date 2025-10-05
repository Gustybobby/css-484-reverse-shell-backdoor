from lib import config, eop_npp as eop, server

if __name__ == "__main__":
    client, ip = server.open_server((config.IP, config.EOP_PORT))
    eop.script(client)
