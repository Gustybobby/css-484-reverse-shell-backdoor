import socket
import json
import debug_util as util


def send(s: socket.socket, data, verbose=False):
    jsondata = json.dumps(data)
    s.send(jsondata.encode())
    util.log(f"[comm:send] {data}", verbose)


def receive(s: socket.socket, bufsize=1024, retry=5, verbose=False):
    data = ""
    count = 0
    while count < retry:
        try:
            data = data + s.recv(bufsize).decode().rstrip()
            util.log(f"[comm:receive] {data}", verbose)
            return json.loads(data)
        except ValueError as e:
            util.log("[comm:receive] error", verbose)
        count += 1
    raise ValueError("error in receive")
