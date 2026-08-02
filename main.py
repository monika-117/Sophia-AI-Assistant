import errno
import os
import socket
import eel
from engine.features import *
from engine.command import *

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
www_dir = os.path.join(script_dir, 'www')


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(('localhost', 0))
        return sock.getsockname()[1]


def _is_port_available(host: str, port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.3)
        return sock.connect_ex((host, port)) != 0


def _start_eel(host: str, port: int) -> None:
    if not _is_port_available('127.0.0.1', port):
        free_port = _find_free_port()
        print(f"Port {port} is already in use; retrying on port {free_port}")
        port = free_port

    try:
        eel.start('index.html', mode=None, host=host, port=port, block=True)
    except OSError as e:
        winerror = getattr(e, 'winerror', None)
        if winerror == 10048 or e.errno in (errno.EADDRINUSE, 10048):
            free_port = _find_free_port()
            print(f"Port {port} is already in use; retrying on port {free_port}")
            eel.start('index.html', mode=None, host=host, port=free_port, block=True)
        else:
            raise

eel.init(www_dir)

# Play start sound if available
try:
	playAssistantSound()
except Exception:
	pass

# Launch a Chrome app window for the UI (optional)
try:
	port = int(os.environ.get('EEL_PORT', '8000'))
except Exception:
	port = 8000
if not _is_port_available('localhost', port):
	port = _find_free_port()
	print(f"Port 8000 is already in use; switching to free port {port}")
try:
	os.system(f'start chrome.exe --app="http://localhost:{port}/index.html"')
except Exception:
	pass

# Start background listeners (hotkey and wake-word) if available
try:
	from engine.hotkey_listener import start_hotkey_listener
	start_hotkey_listener()
except Exception:
	pass

try:
	from engine.wake_word import start_wake_word_listener
	start_wake_word_listener()
except Exception:
	pass

_start_eel('localhost', port)

# command to run

#cd .\sophia-AI-main
#.\envSophia\Scripts\python.exe .\Sophia-AI-Assistant-master\main.py