import time
import re
import os
import pyttsx3
import speech_recognition as sr
import eel

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    #print(voices)
    engine.setProperty('voice', voices[1].id)
    engine.setProperty('rate', 170)
    try:
        if hasattr(eel, 'DisplayMessage'):
            eel.DisplayMessage(text)
    except Exception:
        pass
    engine.say(text)
    engine.runAndWait()


def init_api_services():
    """Initialize external API services after speak() exists."""
    try:
        from engine.config import GEMINI_API_KEY, HUGGINGFACE_API_TOKEN
        from engine.ai_conversation import set_api_keys
        set_api_keys(GEMINI_API_KEY, HUGGINGFACE_API_TOKEN)
    except Exception as e:
        print(f"Error initializing AI services: {e}")

    try:
        from engine.config import WEATHER_API_KEY
        from engine.info_retrieval import set_weather_api_key
        set_weather_api_key(WEATHER_API_KEY)
    except Exception as e:
        print(f"Error initializing weather service: {e}")
    
    try:
        # Calendar integration removed per user request
        pass
    except Exception as e:
        print(f"Error initializing calendar service: {e}")


init_api_services()

@eel.expose
def takeCommand():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print('Listening...')
            try:
                eel.DisplayMessage('Listening...')
            except Exception:
                pass
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source)
            try:
                audio = r.listen(source, timeout=10, phrase_time_limit=6)
            except sr.WaitTimeoutError:
                # no speech detected within timeout
                print('Listening timed out (no phrase)')
                try:
                    eel.DisplayMessage('Listening timed out')
                except Exception:
                    pass
                return ""
    except (AttributeError, OSError):
        # PyAudio or microphone not available — fall back to typed input
        try:
            eel.DisplayMessage('Microphone not available; please type your command.')
        except Exception:
            pass
        try:
            query = input('Microphone not available. Type command (or press Enter to skip): ')
        except Exception:
            return ""
        return query.lower() if query else ""
    
    try:
        print('Recognizing...')
        eel.DisplayMessage('Recognizing...')
        query = r.recognize_google(audio, language='en')
        print(f'User said: {query}')
        #speak(query)
        time.sleep(2)
        eel.DisplayMessage(query)
        
        

    except Exception as e:
        return ""
    
    return query.lower()

# text = takeCommand()

# speak(text)
def route_command(query: str):
    """Route typed and spoken commands through the same feature dispatcher."""
    if not query:
        return ""
    query = query.lower().strip()
    print('Command:', query)

    # ==================== MESSAGING COMMANDS ====================
    if ('send' in query or 'chat' in query or 'message' in query) and ('whatsapp' in query or 'telegram' in query or 'facebook' in query \
            or re.search(r'\+?\d{7,15}', query) or re.search(r'to\s+@?[a-z0-9_]+', query)):
        from engine.features import send_message_from_speech
        send_message_from_speech(query)

    elif 'video call' in query and ('whatsapp' in query or 'telegram' in query or 'facebook' in query):
        from engine.features import video_call
        video_call(query)

    # ==================== ENTERTAINMENT COMMANDS ====================
    elif 'play' in query and 'on youtube' in query:
        from engine.features import PlayYoutube
        PlayYoutube(query)

    # ==================== REMINDER COMMANDS ====================
    elif 'list reminders' in query or 'show reminders' in query or 'what reminders' in query:
        from engine.features import list_reminders
        list_reminders()

    elif 'remind' in query or 'reminder' in query:
        from engine.features import set_reminder_from_query
        set_reminder_from_query(query)

    # ==================== CONTACT MANAGEMENT COMMANDS ====================
    elif 'add contact' in query:
        from engine.contact_manager import add_contact_voice
        add_contact_voice(query)
    
    elif ('list contacts' in query or 'show contacts' in query or 'my contacts' in query):
        from engine.contact_manager import list_contacts_voice
        list_contacts_voice()
    
    elif 'delete contact' in query:
        from engine.contact_manager import delete_contact_voice
        delete_contact_voice(query)

    # ==================== FACE RECOGNITION COMMANDS ====================
    elif 'recognize me' in query or 'face recognition' in query:
        from engine.face_recognition_module import activate_face_recognition
        user = activate_face_recognition()
        if user:
            speak(f"Welcome back, {user}!")
    
    elif 'register face' in query or 'register my face' in query:
        speak("Please tell me your name for registration")
        name = takeCommand()
        if name:
            from engine.face_recognition_module import register_new_user
            register_new_user(name)

    # ==================== INFORMATION RETRIEVAL COMMANDS ====================
    elif 'wikipedia' in query or query.startswith('what is ') or query.startswith('who is ') or query.startswith('search '):
        # Use Wikipedia for information
        from engine.info_retrieval import fetch_wikipedia
        fetch_wikipedia(query)

    elif 'weather' in query:
        # Extract city name if provided, otherwise use default
        city_match = re.search(r'weather\s+(?:in|for)?\s+([a-zA-Z\s]+?)(?:\s+today|\s+tomorrow|$)', query)
        city = city_match.group(1).strip() if city_match else "New York"
        
        if 'forecast' in query:
            from engine.info_retrieval import check_weather_forecast
            check_weather_forecast(city)
        else:
            from engine.info_retrieval import check_weather
            check_weather(city)

    # Calendar commands removed

    # ==================== AI CONVERSATION COMMANDS ====================
    elif any(keyword in query for keyword in ['ask', 'tell me', 'what', 'how', 'why', 'when', 'where']):
        # Use AI for conversation
        from engine.ai_conversation import ask_question
        ask_question(query)

    # ==================== OPEN APPLICATION COMMANDS ====================
    elif 'open' in query or 'notepad' in query or 'youtube' in query or 'github' in query \
            or 'whatsapp' in query or 'instagram' in query or 'calculator' in query \
            or 'facebook' in query or 'telegram' in query or 'canva' in query \
            or 'chrome' in query or 'vscode' in query or 'filemanager' in query \
            or 'command prompt' in query or 'file manager' in query or 'file explorer' in query:
        from engine.features import openCommand
        openCommand(query)
    else:
        try:
            from engine.chat import get_chat_response
            response = get_chat_response(query)
            print('Chat response:', response)
            speak(response)
        except Exception as e:
            print('Chat handling failed:', e)
            print('Not run')

    try:
        eel.ShowHood()
    except Exception:
        pass
    return query


@eel.expose
def allCommands():
    query = takeCommand()
    return route_command(query)


@eel.expose
def processText(query: str):
    """Process a typed text command from the UI (exposed to JS)."""
    return route_command(query)

    
