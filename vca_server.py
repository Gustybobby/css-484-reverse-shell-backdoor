import socket
import threading
import pyaudio
import cv2
import numpy as np
from lib import config

# === Audio Settings ===
FORMAT = pyaudio.paInt16


# === Video Server Thread ===
def video_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((config.IP, config.VDO_PORT))
    s.listen(1)
    print(f"[VIDEO] Listening on {config.IP}:{config.VDO_PORT}")

    conn, addr = s.accept()
    print(f"[VIDEO] connected from {addr}")

    data = b""
    payload_size = 4

    try:
        while True:
            while len(data) < payload_size:
                packet = conn.recv(4096)
                if not packet:
                    raise Exception("[VIDEO] disconnected")
                data += packet

            frame_size = int.from_bytes(data[:payload_size], byteorder="big")
            data = data[payload_size:]

            while len(data) < frame_size:
                data += conn.recv(4096)

            frame_data = data[:frame_size]
            data = data[frame_size:]

            frame = np.frombuffer(frame_data, dtype=np.uint8)
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

            if frame is not None:
                cv2.imshow("Remote Screen", frame)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
    except Exception as e:
        print("[VIDEO] Exception:", e)
    finally:
        conn.close()
        s.close()
        cv2.destroyAllWindows()
        print("[VIDEO] connection closed")


# === Audio Server Thread ===
def audio_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((config.IP, config.AUD_PORT))
    s.listen(1)
    print(f"[AUDIO] Listening on {config.IP}:{config.AUD_PORT}")

    conn, addr = s.accept()
    print(f"[AUDIO] connected from {addr}")

    p = pyaudio.PyAudio()
    stream = p.open(
        format=FORMAT,
        channels=config.CHANNELS,
        rate=config.RATE,
        output=True,
        frames_per_buffer=config.CHUNK,
    )

    try:
        while True:
            data = conn.recv(config.CHUNK * 2)
            if not data:
                break
            stream.write(data)
    except Exception as e:
        print("[AUDIO] Exception:", e)
    finally:
        conn.close()
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("[AUDIO] connection closed")


# === Main Entry ===
if __name__ == "__main__":
    print(
        f"[*] Kali servers running (video={config.VDO_PORT}, audio={config.AUD_PORT}). Press Ctrl+C to stop."
    )
    threading.Thread(target=video_server).start()
    threading.Thread(target=audio_server).start()
