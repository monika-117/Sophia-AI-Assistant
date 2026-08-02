"""
Global hotkey listener using the `keyboard` package.

Registers `Windows+J` to activate the assistant: it will speak a prompt
and start listening for a command using existing `takeCommand()` flow.
"""
import threading

def _on_hotkey():
    try:
        from engine.command import speak, takeCommand, route_command
        speak('Listening')
        query = takeCommand()
        if query:
            route_command(query)
    except Exception as e:
        print('Hotkey handler error:', e)

def start_hotkey_listener():
    try:
        import keyboard
    except Exception as e:
        print('keyboard package not installed; hotkey disabled:', e)
        return

    def run():
        try:
            # Register a global hotkey for Windows+J
            keyboard.add_hotkey('windows+j', _on_hotkey)
            # Block forever, keeping the listener active
            keyboard.wait()
        except Exception as e:
            print('Hotkey listener crashed:', e)

    t = threading.Thread(target=run, daemon=True)
    t.start()
