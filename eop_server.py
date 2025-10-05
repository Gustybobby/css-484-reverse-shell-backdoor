from lib import config
import eop_npp as eop
from lib import server

if __name__ == "__main__":
    client, ip = server.open_server((config.IP, config.EOP_PORT))
    eop.script(client)
