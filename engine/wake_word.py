"""
Simple wake-word listener using SpeechRecognition's background listener.

This is a lightweight approach that uses `recognize_google` to transcribe
short audio snippets and looks for the keyword "sophia". It's less reliable
than dedicated wake-word engines but requires no extra native deps.
"""
import threading

def start_wake_word_listener():
    try:
        import speech_recognition as sr
    except Exception as e:
        print('SpeechRecognition not available; wake-word disabled:', e)
        return None

    recognizer = sr.Recognizer()
    mic = None
    try:
        mic = sr.Microphone()
    except Exception as e:
        print('Microphone not available for wake-word listener:', e)
        return None

    def callback(recognizer, audio):
        try:
            text = recognizer.recognize_google(audio).lower()
            if 'sophia' in text:
                from engine.command import speak, takeCommand, route_command
                speak('Yes?')
                query = takeCommand()
                if query:
                    route_command(query)
        except Exception:
            # ignore recognition errors/no-speech
            pass

    def run():
        stop_listening = recognizer.listen_in_background(mic, callback)
        # keep thread alive
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            stop_listening(wait_for_stop=False)

    t = threading.Thread(target=run, daemon=True)
    t.start()
    return t
