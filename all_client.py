import threading
import eop_client
import klg_client
import vca_client

if __name__ == "__main__":
    eop = threading.Thread(target=eop_client.connect_eop_server)
    klg = threading.Thread(target=klg_client.connect_klg_server)
    vdo = threading.Thread(target=vca_client.send_video)
    aud = threading.Thread(target=vca_client.send_audio)

    eop.start()
    klg.start()
    vdo.start()
    aud.start()

    eop.join()
    klg.join()
    vdo.join()
    aud.join()
