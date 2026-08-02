import os
import re
import sqlite3
import webbrowser
import urllib.parse
import threading
import time
import datetime
import subprocess
from pathlib import Path
try:
    from playsound import playsound
except Exception:
    def playsound(_path):
        return None
try:
    import pyperclip
except Exception:
    pyperclip = None
try:
    import pyautogui
except Exception:
    pyautogui = None
try:
    import cv2
except Exception:
    cv2 = None
import eel

from engine.command import speak
from engine.config import ASSISTANT_NAME
import pywhatkit as kit


conn = sqlite3.connect("sophia.db")
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS reminders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    remind_at TEXT NOT NULL,
    created_at TEXT NOT NULL,
    notified INTEGER NOT NULL DEFAULT 0
)
""")
conn.commit()

# Start background reminder monitoring thread
_thread_started = False

def _start_reminder_monitor():
    global _thread_started
    if _thread_started:
        return
    _thread_started = True

    def monitor():
        conn2 = sqlite3.connect("sophia.db")
        cursor2 = conn2.cursor()
        while True:
            now = datetime.datetime.now().isoformat()
            cursor2.execute("SELECT id, task FROM reminders WHERE notified=0 AND remind_at <= ?", (now,))
            rows = cursor2.fetchall()
            for reminder_id, task in rows:
                try:
                    speak(f"Reminder: {task}")
                except Exception:
                    pass
                try:
                    eel.DisplayMessage(f"Reminder: {task}")
                except Exception:
                    pass
                cursor2.execute("UPDATE reminders SET notified=1 WHERE id=?", (reminder_id,))
                conn2.commit()
            time.sleep(20)

    thread = threading.Thread(target=monitor, daemon=True)
    thread.start()

_start_reminder_monitor()

# sound function for playing sound
BASE_DIR = Path(__file__).resolve().parent.parent
AUDIO_DIR = BASE_DIR / "www" / "assets" / "audio"

def _audio_file(name):
    return str(AUDIO_DIR / name)


def playAssistantSound():
    music_dir = _audio_file("start_sound.mp3")
    try:
        if not Path(music_dir).exists():
            print(f"Start sound file not found: {music_dir}")
            return
        playsound(music_dir)
    except Exception as e:
        print(f"Error playing start sound: {e}")

# click sound for mic button

@eel.expose
def playClickSound():
    music_dir = _audio_file("click_sound.mp3")
    try:
        if not Path(music_dir).exists():
            print(f"Click sound file not found: {music_dir}")
            return
        playsound(music_dir)
    except Exception as e:
        print(f"Error playing click sound: {e}")



def openCommand(query):
    query = query.lower()
    query = query.replace(ASSISTANT_NAME.lower(), "")
    query = query.replace("open", "").strip()

    if not query:
        speak("Please tell me what to open.")
        return
    if 'remind' in query or 'reminder' in query:
        set_reminder_from_query(query)
        return
    if "notepad" in query:
        speak("Opening Notepad")
        os.system("start notepad")
        return

    if any(keyword in query for keyword in ["youtube", "song", "video", "channel"]):
        open_youtube(query)
        return

    if any(keyword in query for keyword in ["github", "instagram", "facebook", "canva"]):
        open_website(query)
        return

    if "whatsapp" in query:
        open_whatsapp(query)
        return

    if "telegram" in query:
        open_telegram(query)
        return

    if any(keyword in query for keyword in ["email", "mail", "gmail", "outlook", "hotmail"]):
        open_email(query)
        return

    if "calculator" in query:
        speak("Opening Calculator")
        os.system("start calc")
        return

    if "chrome" in query:
        speak("Opening Google Chrome")
        os.system("start chrome")
        return

    if "vscode" in query or "visual studio code" in query:
        speak("Opening VS Code")
        os.system("start code")
        return

    if any(term in query for term in ["filemanager", "file manager", "file explorer"]):
        speak("Opening File Explorer")
        os.system("start explorer")
        return

    if any(term in query for term in ["commandprompt", "command prompt", "cmd"]):
        speak("Opening Command Prompt")
        os.system("start cmd")
        return

    speak("Opening " + query)
    os.system(f"start {query}")


def open_website(query):
    if "github" in query:
        speak("Opening GitHub")
        webbrowser.open("https://github.com")
        return
    if "instagram" in query:
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")
        return
    if "facebook" in query:
        speak("Opening Facebook")
        webbrowser.open("https://www.facebook.com")
        return
    if "canva" in query:
        speak("Opening Canva")
        webbrowser.open("https://www.canva.com")
        return


def open_whatsapp(query):
    if "send" in query or "message" in query:
        send_whatsapp_text(query)
        return

    speak("Opening WhatsApp")
    webbrowser.open("https://web.whatsapp.com")


def open_telegram(query):
    if "send" in query or "message" in query:
        send_telegram_text(query)
        return

    speak("Opening Telegram")
    webbrowser.open("https://web.telegram.org")


def open_email(query: str):
    """Open an email client or webmail based on query keywords.

    Supports Gmail and Outlook web UIs, attempts to open Outlook desktop if
    requested, and falls back to the system default mail handler (mailto:).
    """
    q = query.lower()
    # Compose or new email
    if any(k in q for k in ("compose", "new email", "send email", "write email")) or "compose" in q:
        try:
            speak("Opening compose window in your default mail client")
        except Exception:
            pass
        try:
            os.startfile('mailto:')
        except Exception:
            webbrowser.open('https://mail.google.com/mail/u/0/#inbox?compose=new')
        return

    if "gmail" in q:
        speak("Opening Gmail")
        webbrowser.open("https://mail.google.com")
        return

    if any(k in q for k in ("outlook", "hotmail", "office")):
        # Try Outlook web first
        speak("Opening Outlook")
        try:
            webbrowser.open("https://outlook.office.com")
        except Exception:
            try:
                os.startfile('outlook')
            except Exception:
                pass
        return

    # Generic mail open: try default mail client, then Gmail web
    try:
        speak("Opening your default mail application")
    except Exception:
        pass
    try:
        os.startfile('mailto:')
    except Exception:
        webbrowser.open('https://mail.google.com')


def open_youtube(query):
    query = query.lower()
    query = query.replace("open", "")
    query = query.replace("youtube", "")
    query = query.replace("on youtube", "")
    query = query.replace("song", "")
    query = query.replace("video", "")
    query = query.replace("channel", "")
    query = query.replace("play", "")
    query = query.replace("search", "")
    query = query.replace("for", "")
    search_term = re.sub(r"\s+", " ", query).strip()

    if not search_term:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
        return

    speak("Opening YouTube search for " + search_term)
    url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote_plus(search_term)
    webbrowser.open(url)


def set_reminder_from_query(query):
    task, remind_at = parse_reminder_query(query)
    if not task or not remind_at:
        speak("Please say something like remind me to call mom at 6 pm or remind me in 10 minutes to check the oven.")
        return

    cursor.execute(
        "INSERT INTO reminders (task, remind_at, created_at) VALUES (?, ?, ?)",
        (task, remind_at.isoformat(), datetime.datetime.now().isoformat()),
    )
    conn.commit()
    speak(f"Reminder set for {remind_at.strftime('%Y-%m-%d %I:%M %p')}: {task}")
    try:
        eel.DisplayMessage(f"Reminder set for {remind_at.strftime('%Y-%m-%d %I:%M %p')}: {task}")
    except Exception:
        pass


def list_reminders():
    cursor.execute("SELECT id, task, remind_at FROM reminders WHERE notified=0 ORDER BY remind_at")
    rows = cursor.fetchall()
    if not rows:
        speak("You have no pending reminders.")
        return

    reminder_texts = []
    for reminder_id, task, remind_at in rows:
        remind_dt = datetime.datetime.fromisoformat(remind_at)
        reminder_texts.append(f"{task} at {remind_dt.strftime('%Y-%m-%d %I:%M %p')}")

    message = "You have " + str(len(rows)) + " pending reminders: " + ", ".join(reminder_texts[:3])
    if len(rows) > 3:
        message += ", and more." 
    speak(message)
    try:
        eel.DisplayMessage(message)
    except Exception:
        pass


def parse_reminder_query(query):
    q = query.lower().strip()
    now = datetime.datetime.now()
    remind_at = None

    # relative time: in X minutes / hours
    rel = re.search(r'in\s+(\d+)\s+(minute|minutes|hour|hours)', q)
    if rel:
        value = int(rel.group(1))
        unit = rel.group(2)
        if 'hour' in unit:
            remind_at = now + datetime.timedelta(hours=value)
        else:
            remind_at = now + datetime.timedelta(minutes=value)

    # explicit today/tomorrow time
    if remind_at is None:
        when_match = re.search(r'(?:tomorrow\s+at|at)\s+(\d{1,2}(?::\d{2})?\s*(?:am|pm)?)', q)
        if when_match:
            time_text = when_match.group(1).strip()
            try:
                remind_time = _parse_time(time_text)
                remind_at = now.replace(hour=remind_time.hour, minute=remind_time.minute, second=0, microsecond=0)
                if 'tomorrow' in q or remind_at <= now:
                    remind_at += datetime.timedelta(days=1)
            except ValueError:
                remind_at = None

    if remind_at is None:
        return None, None

    task = re.sub(r'.*remind me(?: to)?\s+', '', q)
    task = re.sub(r'\s+at\s+\d{1,2}(?::\d{2})?\s*(?:am|pm)?', '', task)
    task = re.sub(r'\s+in\s+\d+\s+(?:minutes?|hours?)', '', task)
    task = re.sub(r'\btomorrow\b', '', task)
    task = task.strip()
    return task, remind_at


def _parse_time(text):
    text = text.strip().lower()
    if re.match(r'^\d{1,2}:\d{2}\s*(am|pm)$', text):
        return datetime.datetime.strptime(text, '%I:%M %p').time()
    if re.match(r'^\d{1,2}\s*(am|pm)$', text):
        return datetime.datetime.strptime(text, '%I %p').time()
    if re.match(r'^\d{1,2}:\d{2}$', text):
        return datetime.datetime.strptime(text, '%H:%M').time()
    if re.match(r'^\d{1,2}$', text):
        return datetime.datetime.strptime(text, '%H').time()
    raise ValueError('Invalid time format')


def infer_message_service(query_lower):
    if "facebook" in query_lower:
        return "facebook"
    if "telegram" in query_lower:
        return "telegram"
    if "whatsapp" in query_lower:
        return "whatsapp"
    if re.search(r'to\s+@?[a-z0-9_]+', query_lower):
        return "telegram"
    if re.search(r'\+?\d{7,15}', query_lower):
        return "whatsapp"
    return None


def send_message_from_speech(query):
    query_lower = query.lower()
    video_call_requested = bool(re.search(r'\band\s+(?:do\s+)?video call\b', query_lower))
    if video_call_requested:
        send_query = re.sub(r'\s+and\s+(?:do\s+)?video call\b.*', '', query_lower).strip()
    else:
        send_query = query_lower

    service = infer_message_service(send_query)
    if service == "whatsapp":
        send_whatsapp_text(send_query)
    elif service == "telegram":
        send_telegram_text(send_query)
    elif service == "facebook":
        send_facebook_text(send_query)
    else:
        speak("I can send messages through WhatsApp, Telegram, or Facebook.")

    if video_call_requested:
        video_call(query_lower)


def strip_video_call_suffix(text):
    return re.sub(r'\s+and\s+(?:do\s+)?video call\b.*$', '', text).strip()


def parse_whatsapp_query(query):
    # chat how r u to 8548936581
    phone_match = re.search(r'to\s+(\+?[0-9]{7,15})', query)
    if phone_match:
        phone = phone_match.group(1)
        prefix = query[:phone_match.start()]
        suffix = query[phone_match.end():]
        message = suffix.strip() or prefix
        message = re.sub(r'\b(chat|send|whatsapp|message|to)\b', '', message).strip()
        return phone, strip_video_call_suffix(message)
    # fallback: whatsapp message to ...
    phone_match = re.search(r'whatsapp\s+message\s+to\s+(\+?[0-9]{7,15})', query)
    if phone_match:
        phone = phone_match.group(1)
        message = re.sub(r'whatsapp\s+message\s+to\s+' + re.escape(phone), '', query).strip()
        return phone, strip_video_call_suffix(message)
    return None, None


def parse_contact_message_query(query):
    """Extract contact name and message from commands like 'send whatsapp message to mom hello'."""
    match = re.search(
        r'(?:send|chat|message)\s+(?:a\s+)?(?:whatsapp\s+)?(?:message\s+)?to\s+([a-zA-Z][a-zA-Z\s]*?)(?:\s+(?:saying|that|message)\s+|\s+)(.+)$',
        query,
    )
    if not match:
        return None, None
    name = match.group(1).strip()
    message = strip_video_call_suffix(match.group(2).strip())
    return name, message


def send_whatsapp_text(query):
    phone, message = parse_whatsapp_query(query)
    contact_name = None

    if not phone and not message:
        # allow plain message with explicit phone later
        phone_match = re.search(r'\+?[0-9]{7,15}', query)
        if phone_match:
            phone = phone_match.group(0)
            message = strip_video_call_suffix(re.sub(re.escape(phone), '', query)).strip()

    # Try to resolve contact name to phone number
    if not phone:
        contact_name, contact_message = parse_contact_message_query(query)
        if contact_name:
            try:
                from engine.contact_manager import get_contact_phone
                phone = get_contact_phone(contact_name)
                message = contact_message or message
                if phone:
                    speak(f"Sending message to {contact_name}")
            except Exception as e:
                print(f"Contact lookup failed: {e}")

    if not phone:
        if contact_name:
            speak(f"I could not find a saved phone number for {contact_name}.")
            return
        speak("Please say send whatsapp message to plus phone number followed by the message.")
        return

    url = "https://web.whatsapp.com/send?"
    if phone:
        url += "phone=" + urllib.parse.quote_plus(phone)
    if message:
        url += "&text=" + urllib.parse.quote_plus(message)
    speak("Opening WhatsApp chat")
    webbrowser.open(url)


def parse_telegram_query(query):
    username_match = re.search(r'to\s+@?([a-z0-9_]+)', query)
    if username_match:
        username = username_match.group(1)
        prefix = query[:username_match.start()]
        suffix = query[username_match.end():]
        message = suffix.strip() or prefix
        message = re.sub(r'\b(chat|send|telegram|message|to)\b', '', message).strip()
        return username, strip_video_call_suffix(message)
    return None, None


def parse_facebook_query(query):
    phone_match = re.search(r'to\s+(\+?[0-9]{7,15})', query)
    if phone_match:
        phone = phone_match.group(1)
        prefix = query[:phone_match.start()]
        suffix = query[phone_match.end():]
        message = suffix.strip() or prefix
        message = re.sub(r'\b(chat|send|facebook|message|to)\b', '', message).strip()
        return phone, strip_video_call_suffix(message)
    username_match = re.search(r'to\s+@?([a-z0-9_.-]+)', query)
    if username_match:
        username = username_match.group(1)
        prefix = query[:username_match.start()]
        suffix = query[username_match.end():]
        message = suffix.strip() or prefix
        message = re.sub(r'\b(chat|send|facebook|message|to)\b', '', message).strip()
        return username, strip_video_call_suffix(message)
    return None, None


def send_facebook_text(query):
    target, message = parse_facebook_query(query)
    if not target and not message:
        speak("Please say chat on facebook to a username or phone number with the message.")
        return

    if re.match(r'^\+?[0-9]{7,15}$', target or ''):
        speak(f"Opening Facebook Messenger chat for {target}")
        webbrowser.open(f"https://www.messenger.com/t/{urllib.parse.quote_plus(target)}")
    else:
        speak(f"Opening Facebook Messenger chat with {target}")
        webbrowser.open(f"https://www.messenger.com/t/{urllib.parse.quote_plus(target)}")

    if message:
        speak("Message text detected: " + message)


def send_telegram_text(query):
    username, message = parse_telegram_query(query)
    if username and not message:
        # if no explicit message, use everything before username
        message = strip_video_call_suffix(re.sub(r'to\s+@?' + re.escape(username), '', query)).strip()

    if username and message:
        speak(f"Opening Telegram chat with {username}")
        webbrowser.open(f"https://t.me/{urllib.parse.quote_plus(username)}?text=" + urllib.parse.quote_plus(message))
    elif username:
        speak(f"Opening Telegram chat with {username}")
        webbrowser.open(f"https://web.telegram.org/k/#@{username}")
    elif message:
        speak("Opening Telegram share link")
        webbrowser.open("https://t.me/share/url?url=&text=" + urllib.parse.quote_plus(message))
    else:
        speak("Please say send telegram message to username followed by the message.")


def video_call(query):
    whatsapp_phone = None
    telegram_username = None

    whatsapp_match = re.search(r'video call\s+whatsapp\s+to\s+(\+?[0-9]+)', query)
    telegram_match = re.search(r'video call\s+telegram\s+to\s+@?([a-z0-9_]+)', query)

    if whatsapp_match:
        whatsapp_phone = whatsapp_match.group(1)
    if telegram_match:
        telegram_username = telegram_match.group(1)

    if not whatsapp_phone and "whatsapp" in query:
        phone_match = re.search(r'\b(\+?[0-9]{7,15})\b', query)
        if phone_match:
            whatsapp_phone = phone_match.group(1)
        else:
            contact_name = extract_call_contact_name(query, "whatsapp")
            if contact_name:
                try:
                    from engine.contact_manager import get_contact_phone
                    whatsapp_phone = get_contact_phone(contact_name)
                    if not whatsapp_phone:
                        speak(f"I could not find a saved phone number for {contact_name}.")
                        return
                except Exception as e:
                    print(f"Contact lookup failed: {e}")

    if not telegram_username and "telegram" in query:
        username_match = re.search(r'to\s+@?([a-z0-9_]+)', query)
        if username_match:
            telegram_username = username_match.group(1)

    if whatsapp_phone:
        start_whatsapp_video_call(whatsapp_phone)
        return
    if telegram_username:
        speak("Opening Telegram chat for video call")
        webbrowser.open(f"https://web.telegram.org/k/#@{telegram_username}")
        return
    if "facebook" in query:
        fb_target = None
        fb_phone_match = re.search(r'to\s+(\+?[0-9]{7,15})', query)
        fb_username_match = re.search(r'to\s+@?([a-z0-9_.-]+)', query)
        if fb_phone_match:
            fb_target = fb_phone_match.group(1)
        elif fb_username_match:
            fb_target = fb_username_match.group(1)

        if fb_target:
            speak("Opening Facebook Messenger chat for video call")
            webbrowser.open("https://www.messenger.com/t/" + urllib.parse.quote_plus(fb_target))
            return
        speak("Opening Facebook Messenger for video call. Please select your contact and start the call.")
        webbrowser.open("https://www.messenger.com")
        return

    if "whatsapp" in query:
        speak("Opening WhatsApp for video call. Please select your contact and start the call.")
        webbrowser.open("https://web.whatsapp.com")
        return
    if "telegram" in query:
        speak("Opening Telegram for video call. Please select your contact and start the call.")
        webbrowser.open("https://web.telegram.org")
        return
    speak("Please say video call whatsapp, telegram, or facebook to a phone number or username.")


def extract_call_contact_name(query, service):
    pattern = rf'video call\s+{service}\s+to\s+([a-zA-Z][a-zA-Z\s]+)$'
    match = re.search(pattern, query)
    if match:
        return match.group(1).strip()

    pattern = rf'video call\s+to\s+([a-zA-Z][a-zA-Z\s]+)\s+on\s+{service}'
    match = re.search(pattern, query)
    if match:
        return match.group(1).strip()
    return None


def start_whatsapp_video_call(phone):
    """Open a WhatsApp chat and try to press the video-call button."""
    clean_phone = re.sub(r'\D', '', phone)
    if not clean_phone:
        speak("Please provide a valid phone number for the WhatsApp video call.")
        return

    speak("Opening WhatsApp chat and starting video call")
    desktop_url = "whatsapp://send?phone=" + urllib.parse.quote_plus(clean_phone)
    web_url = "https://web.whatsapp.com/send?phone=" + urllib.parse.quote_plus(clean_phone)

    try:
        os.startfile(desktop_url)
    except Exception:
        webbrowser.open(web_url)

    thread = threading.Thread(target=click_whatsapp_video_button, daemon=True)
    thread.start()


def click_whatsapp_video_button():
    """Best-effort click for the WhatsApp video-call button.

    WhatsApp does not provide a direct public URL for starting a video call.
    This opens the chat first, then clicks the video icon near the chat header.
    """
    if pyautogui is None:
        speak("WhatsApp chat is open. PyAutoGUI is not installed, so please click the video call button.")
        return

    try:
        time.sleep(8)
        pyautogui.hotkey('win', 'up')
        time.sleep(1)
        width, _height = pyautogui.size()

        # WhatsApp Desktop/Web places the call controls near the top-right of the chat header.
        click_points = [
            (width - 180, 92),
            (width - 220, 92),
            (width - 260, 92),
        ]
        for x, y in click_points:
            pyautogui.click(x, y)
            time.sleep(1.5)

        speak("I tried to start the WhatsApp video call. If a permission prompt appears, please allow camera and microphone.")
    except Exception as e:
        print(f"Could not click WhatsApp video button: {e}")
        speak("I opened the WhatsApp chat. Please click the video call button at the top.")


def PlayYoutube(query):
    search_term = extract_yt_term(query)
    if search_term:
        speak("Playing " + search_term + " on YouTube")
        kit.playonyt(search_term)
    else:
        speak("Sorry, I couldn't find what to play on YouTube.")


def extract_yt_term(command):
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    match = re.search(pattern, command, re.IGNORECASE)
    return match.group(1) if match else None
