import os
import pyaudio
import wave
from . import config

frames = []


def record(cycle_size: int):
    if not os.path.exists(config.CLIENT_AUDIO_DIR):
        os.mkdir(config.CLIENT_AUDIO_DIR)

    fps = int(config.RATE / config.FPB * config.DURATION)

    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=config.CHANNELS,
        rate=config.RATE,
        input=True,
        frames_per_buffer=config.FPB,
        stream_callback=callback,
    )
    stream.start_stream()

    count = 0
    try:
        while True:
            if len(frames) > fps:
                clip = []
                for i in range(0, fps):
                    clip.append(frames[i])
                fname = f"{config.CLIENT_AUDIO_DIR}/{str(count % cycle_size)}.wav"
                wavefile = config_wav(fname, p)
                wavefile.writeframes(b"".join(clip))
                wavefile.close()
                frames = frames[config.DURATION - 1 :]
                count += 1
    except Exception as e:
        print("[AUDIO_CLIENT_ERROR]", e)
        stream.stop_stream()


def callback(in_data, frame_count, time_info, status):
    frames.append(in_data)
    return in_data, pyaudio.paContinue


def config_wav(filename, p: pyaudio.PyAudio):
    wavefile = wave.open(filename, "wb")
    wavefile.setnchannels(config.CHANNELS)
    wavefile.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wavefile.setframerate(config.RATE)
    return wavefile
