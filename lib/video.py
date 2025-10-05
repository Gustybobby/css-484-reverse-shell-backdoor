import os
import time
import pyautogui
from lib import config


def create_client_dir():
    if not os.path.exists(config.CLIENT_SCREENSHOT_DIR):
        os.mkdir(config.CLIENT_SCREENSHOT_DIR)


def capture(frame: int):
    image = pyautogui.screenshot()
    image.save(f"{config.CLIENT_SCREENSHOT_DIR}/{str(frame)}.png")


def record(cycle_size: int):
    try:
        create_client_dir()
        count = 0
        while True:
            capture(count % cycle_size)
            time.sleep(1)
            count += 1
    except Exception as e:
        print("[VIDEO_CLIENT_ERROR]", e)
