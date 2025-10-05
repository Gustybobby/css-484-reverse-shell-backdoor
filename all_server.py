import threading
import eop_server
import klg_server
import vca_server

if __name__ == "__main__":
    eop = threading.Thread(target=eop_server.open_eop_server)
    klg = threading.Thread(target=klg_server.open_klg_server)
    vdo = threading.Thread(target=vca_server.open_video_server)
    aud = threading.Thread(target=vca_server.open_audio_server)

    eop.start()
    klg.start()
    vdo.start()
    aud.start()

    eop.join()
    klg.join()
    vdo.join()
    aud.join()
