# Sophia AI Assistant
Sophia is a desktop AI assistant built using Python that can perform various tasks such as answering questions like ChatGPT, opening desktop applications, browsing websites, and even making phone and WhatsApp calls. This project is designed to be versatile and extensible, with the ability to add more functionalities easily. It integrates the Hugging Face API, a free ChatGPT alternative to simulate conversation, and offers multiple activation methods for user commands.

## Google Calendar Setup

To enable Google Calendar integration:

- Install required packages from `requirements.txt` (includes `google-api-python-client` and `google-auth-oauthlib`).
- Create a Google Cloud project, enable the Calendar API, and create an OAuth 2.0 Client ID for a "Desktop application".
- Download the credentials JSON and place it in the project root as `credentials.json`.
- On first run, the application will open a browser window to authorize access and will save `token.json` for future runs.

See [API_INTEGRATION_GUIDE.md](API_INTEGRATION_GUIDE.md) for full details.

### Re-authorize or check calendar from voice/CLI

- Say "configure calendar", "setup calendar" or "connect calendar" to force re-authentication.
- Say "calendar status" to hear whether `credentials.json`, `token.json`, and the calendar service are present.
- You can also run re-auth from a Python shell:

```powershell
python -c "from engine.calendar_cli import reauth_calendar; print(reauth_calendar())"
```

## Activation Options

- **Text input:** Type a command and press Enter in the input box.
- **Mic button:** Click the microphone button — Sophia will listen and respond.
- **Wake word:** Say "Sophia" (experimental). A background listener attempts to detect the wake word and will prompt to listen. This uses the `SpeechRecognition` library and `recognize_google` by default; reliability depends on your microphone and internet connection.
- **Global hotkey (Windows):** Press `Windows + J` to activate listening. This requires the `keyboard` package and may require elevated privileges on some systems.

If you want the hotkey or wake-word disabled, remove or comment out the imports in `main.py` that start `engine.hotkey_listener` and `engine.wake_word`.

