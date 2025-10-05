import os


def debug(msg: str, verbose: bool):
    if verbose:
        print(f"[PID:{os.getpid()}]", msg)
