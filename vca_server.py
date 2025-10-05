import socket
import time
from datetime import datetime
import io
import pyaudio
from PIL import Image
from lib import comm, config, server


def video_receiver(client: socket.socket):
    try:
        while True:
            data = comm.multireceive(client, config.SERVER_VERBOSE)
            image = Image.open(io.BytesIO(data))
            formatted_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            image.save(f"{config.SCREENSHOT_DIR}/{formatted_time}.png")
            time.sleep(1)
    except:
        pass


def audio_receiver(client: socket.socket):
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
            data = comm.multireceive(client, config.SERVER_VERBOSE)
            if not data:
                continue
            stream.write(data)
            time.sleep(1)
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()


def open_video_server():
    client, _ = server.open_server((config.IP, config.VDO_PORT))
    video_receiver(client)


def open_audio_server():
    client, _ = server.open_server((config.IP, config.AUD_PORT))
    audio_receiver(client)
