import threading


def debug(msg: str, verbose: bool):
    if verbose:
        print(f"[TID:{threading.get_native_id()}]", msg)
