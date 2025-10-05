import socket
import cv2
import numpy as np
import pyautogui
import pyaudio
import time
from lib import config


# =====================
# Screen Capture Sender
# =====================
def send_video():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((config.IP, config.VDO_PORT))
        print(f"[VIDEO] Connected to {config.IP}:{config.VDO_PORT}")

        while True:
            # Screenshot full screen
            screenshot = pyautogui.screenshot()

            # Convert to OpenCV format
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            frame = cv2.resize(frame, (config.FRAME_WIDTH, config.FRAME_HEIGHT))

            # Encode image as JPEG
            _, buffer = cv2.imencode(".jpg", frame)

            # Send size then image
            size = len(buffer)
            sock.sendall(size.to_bytes(4, byteorder="big"))
            sock.sendall(buffer)  # type: ignore

            time.sleep(0.1)  # reduce CPU usage
    except Exception as e:
        print(f"[VIDEO] Error: {e}")
    finally:
        sock.close()
        print("[VIDEO] Connection closed.")


# =====================
# Microphone Audio Sender
# =====================
def send_audio():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((config.IP, config.AUD_PORT))
        print(f"[AUDIO] Connected to {config.IP}:{config.AUD_PORT}")

        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=44100,
            input=True,
            frames_per_buffer=1024,
        )

        while True:
            data = stream.read(1024)
            sock.sendall(data)
    except Exception as e:
        print(f"[AUDIO] Error: {e}")
    finally:
        sock.close()
        print("[AUDIO] Connection closed.")
