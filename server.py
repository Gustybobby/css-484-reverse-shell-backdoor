from lib import server_call as server
import npp_eop as eop

if __name__ == "__main__":
    client, ip = server.open_server()
    eop.event_loop(client)
