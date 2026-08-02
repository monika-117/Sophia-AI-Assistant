"""
Sophia AI Assistant Configuration
Set API keys through environment variables when possible.
"""
import os

ASSISTANT_NAME = 'Sophia'

# ==================== API KEYS ====================
# Google Gemini API Key
# Get from: https://ai.google.dev/
GEMINI_API_KEY = os.environ.get("GOOGLE_API_KEY", "")

# Hugging Face API Token
# Get from: https://huggingface.co/settings/tokens
HUGGINGFACE_API_TOKEN = os.environ.get("HF_API_TOKEN", "")

# OpenWeather API Key
# Get from: https://openweathermap.org/api
WEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY", "")

# Google Calendar API
# Get from: https://developers.google.com/calendar/api
GOOGLE_CALENDAR_CREDENTIALS_FILE = "credentials.json"

# ==================== SETTINGS ====================
# Default location for weather
DEFAULT_LOCATION = "New York"

# Voice settings
VOICE_RATE = 170  # Speed of voice (50-300)
VOICE_VOLUME = 1.0  # Volume (0.0-1.0)

# Face recognition settings
FACE_RECOGNITION_ENABLED = True
FACE_RECOGNITION_CONFIDENCE_THRESHOLD = 70

# ==================== FEATURE FLAGS ====================
ENABLE_FACE_RECOGNITION = True
ENABLE_VOICE_CONTROL = True
ENABLE_AI_CONVERSATION = True
ENABLE_WEATHER = True
ENABLE_CALENDAR = False
ENABLE_CONTACTS = True
ENABLE_WHATSAPP_INTEGRATION = True
