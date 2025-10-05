import socket
import time
import communication as comm
import command as cmd


def event_loop(s: socket.socket):
    found_npp = False
    while True:
        time.sleep(2)
        if found_npp:
            pass
        else:
            comm.send(s, 'exec [tasklist | findstr /I "npp"]')
            result = cmd.recv_exec_command(s)
            print(result)
