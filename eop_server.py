from lib import config, server_call as server
import eop_npp as eop

if __name__ == "__main__":
    client, ip = server.open_server((config.IP, config.EOP_PORT))
    eop.script(client)
