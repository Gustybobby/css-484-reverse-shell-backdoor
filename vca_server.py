import socket
import time
from lib import config, server


def video_receiver(client: socket.socket):
    while True:
        time.sleep(1)


def audio_receiver(client: socket.socket):
    while True:
        time.sleep(1)


def open_video_server():
    client, _ = server.open_server((config.IP, config.VDO_PORT))
    video_receiver(client)


def open_audio_server():
    client, _ = server.open_server((config.IP, config.AUD_PORT))
    audio_receiver(client)


if __name__ == "__main__":
    open_video_server()
    open_audio_server()
