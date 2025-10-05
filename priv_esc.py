import socket
import time
import communication as comm
import command as cmd


def find_npp_dir(s: socket.socket) -> str:
    comm.send(s, "exec [where /r C:\\Users *npp*]")
    result = cmd.recv_exec_command(s)
    print(f"'{result}'")
    return result


def handle_found_npp(s: socket.socket):
    res = find_npp_dir(s)
    time.sleep(5)
    dir = "\\".join(res.split("\\")[:-1])
    print(dir)
    pass


def event_loop(s: socket.socket):
    found_npp = False
    while True:
        time.sleep(2)
        if found_npp:
            break
        else:
            comm.send(s, 'exec [tasklist | findstr /I "npp"]')
            result = cmd.recv_exec_command(s)
            print(result)
            found_npp = True

    handle_found_npp(s)
