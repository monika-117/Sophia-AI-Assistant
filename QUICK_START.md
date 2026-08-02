# Sophia AI Assistant - Quick Start Guide

## Fast Setup (5 Minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Configure API Keys
Open `engine/config.py` and add your API keys:

#### Get Gemini API Key (Free):
- Go to https://ai.google.dev/
- Click "Get API Key"
- Paste key in config.py:
```python
GEMINI_API_KEY = "paste_your_key_here"
```

#### Get Weather API Key (Free):
- Go to https://openweathermap.org/api
- Sign up (free tier available)
- Paste key in config.py:
```python
WEATHER_API_KEY = "paste_your_key_here"
```

#### Optional - Hugging Face Token:
- Go to https://huggingface.co/settings/tokens
- Create new token
- Paste in config.py:
```python
HUGGINGFACE_API_TOKEN = "paste_your_token_here"
```

### Step 3: Run the Application
```bash
python main.py
```

---

## Try These Commands First

After starting the app, say these voice commands:

### 1. Add a Contact
```
"Add contact mom as plus one nine one nine nine nine nine nine nine nine"
```

### 2. Ask a Question
```
"What is artificial intelligence?"
```

### 3. Check Weather
```
"Weather in New York"
```

### 4. Register Your Face
```
"Register face"
(Then say your name and look at the camera)
```

### 5. Set a Reminder
```
"Remind me to call mom in 10 minutes"
```


## Common Issues & Fixes

**Problem**: "API key not configured"
- **Fix**: Add the key to `engine/config.py` and restart

**Problem**: Camera not working
- **Fix**: Close other apps using webcam, check permissions

**Problem**: Microphone not detected
- **Fix**: Check audio input device in Windows settings

**Problem**: "No module named..."
- **Fix**: Run `pip install -r requirements.txt` again

---

## Next Steps

1.  Basic setup done!
2.  Add more contacts for easier messaging
3.  Register multiple users for face recognition
4.  Set up Google Calendar (optional)
5.  Customize voice settings in `engine/config.py`

---

**You're all set! Start using Sophia by pressing the microphone button or saying voice commands.** 
