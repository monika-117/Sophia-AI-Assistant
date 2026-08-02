# API Integration Guide

## Overview
This guide explains how to set up and integrate the various APIs used by Sophia AI Assistant.

---

## 1. Google Gemini API (AI Conversations)

### Why Use It?
- Free tier available
- Powerful language model
- Great for question answering and general knowledge

### Setup Steps

1. **Get API Key**
   - Visit https://ai.google.dev/
   - Click "Get API Key" button
   - Create a new project if needed
   - Generate the API key

2. **Configure in Sophia**
   ```python
   # engine/config.py
   GEMINI_API_KEY = "your_api_key_here"
   ```

3. **Test It**
   ```
   Say: "What is Python?"
   Sophia will provide an answer using Gemini
   ```


### Docs
https://ai.google.dev/tutorials/python_quickstart

---

## 2. OpenWeather API (Weather Updates)

### Why Use It?
- Real-time weather data
- Accurate forecasts
- Covers entire world

### Setup Steps

1. **Create Account**
   - Visit https://openweathermap.org/
   - Click "Sign Up"
   - Complete registration

2. **Get API Key**
   - Log in to your account
   - Go to API keys section
   - Copy your API key

3. **Configure in Sophia**
   ```python
   # engine/config.py
   WEATHER_API_KEY = "your_api_key_here"
   DEFAULT_LOCATION = "New York"  # Optional default city
   ```

4. **Test It**
   ```
   Say: "Weather in London"
   Sophia will provide current weather and conditions
   ```

### Features Available
- Current weather
- Temperature (Celsius/Fahrenheit)
- Humidity and wind speed
- Weather description
- 5-day forecast

### Rate Limits (Free Tier)
- 1,000 calls per day
- 60 calls per minute

### Cost
- **Free**: 1,000 calls/day
- **Paid**: Scaling plans available

### Docs
https://openweathermap.org/api

---

## 3. Hugging Face API (Alternative AI)

### Why Use It?
- Alternative to Gemini
- Different models available
- Good for creative tasks

### Setup Steps

1. **Create Account**
   - Visit https://huggingface.co/
   - Click "Sign Up"
   - Complete registration

2. **Get API Token**
   - Go to https://huggingface.co/settings/tokens
   - Click "New token"
   - Generate and copy token

3. **Configure in Sophia**
   ```python
   # engine/config.py
   HUGGINGFACE_API_TOKEN = "your_token_here"
   ```

4. **Test It**
   ```
   Say: "Ask hugging face what is AI?"
   Sophia will query Hugging Face
   ```

### Available Models
- gpt2 (Conversational)
- distilgpt2 (Lighter version)
- text-davinci-003 (Powerful - requires paid API)
- Many others available

### Rate Limits
- Varies by model
- Generally 50-100 requests per minute for free tier

### Cost
- **Free**: Limited usage
- **Paid**: Starting from $9/month

### Docs
https://huggingface.co/docs/hub/security-tokens

---

## 4. Google Calendar API (Calendar Events)

### Why Use It?
- Sync with your Google Calendar
- Check upcoming events by voice
- Integration with Google ecosystem

### Setup Steps (Advanced)

1. **Create Google Cloud Project**
   - Visit https://console.cloud.google.com/
   - Create a new project
   - Name it "Sophia"

2. **Enable Calendar API**
   - In Google Cloud Console
   - Search for "Calendar API"
   - Click "Enable"

3. **Create OAuth Credentials**
   - Go to "Credentials" section
   - Click "Create Credentials" → "OAuth 2.0 Client ID"
   - Choose "Desktop application"
   - Download the credentials file

4. **Place Credentials File**
   ```
   Place the downloaded JSON file in project root as: credentials.json
   ```

5. **First Run**
   - Run Sophia application
   - A browser window will open for authentication
   - Log in with your Google account
   - Grant permissions
   - Token is saved for future use

6. **Test It**
   ```
   Say: "Show my calendar"
   Sophia will list upcoming events
   ```

### Docs
https://developers.google.com/calendar/api

---

## 5. System Requirements for Advanced Features

### Face Recognition
- **Requirements**:
  - Webcam (built-in or USB)
  - Good lighting for registration
  - OpenCV (included in requirements.txt)

- **Performance**:
  - Registration: ~30 seconds per person
  - Recognition: ~2-3 seconds
  - Accuracy: 85-95% with good lighting

### Voice Recognition
- **Requirements**:
  - Microphone (built-in or USB)
  - SpeechRecognition library (included)
  - Google Speech API (free, included with library)

- **Performance**:
  - Recognition time: 2-5 seconds
  - Supports: English, Spanish, French, German, etc.

---

## 6. Environment Setup

### Using Environment Variables (Recommended for Security)

Instead of hardcoding API keys in config.py, use environment variables:

```python
# engine/config.py
import os

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', 'YOUR_DEFAULT_KEY')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', 'YOUR_DEFAULT_KEY')
HUGGINGFACE_API_TOKEN = os.getenv('HUGGINGFACE_API_TOKEN', 'YOUR_DEFAULT_TOKEN')
```

### Set Environment Variables (Windows)

**Option 1: Command Line**
```bash
set GEMINI_API_KEY=your_key_here
set WEATHER_API_KEY=your_key_here
set HUGGINGFACE_API_TOKEN=your_token_here
python main.py
```

**Option 2: .env File**
Create `.env` file in project root:
```
GEMINI_API_KEY=your_key_here
WEATHER_API_KEY=your_key_here
HUGGINGFACE_API_TOKEN=your_token_here
```

Then use python-dotenv to load:
```python
from dotenv import load_dotenv
load_dotenv()
```

---


## 8. Troubleshooting APIs

### Gemini Not Responding
```
Issue: "Unable to get response from Gemini"
Fix 1: Check API key is correct
Fix 2: Check internet connection
Fix 3: Check rate limits aren't exceeded
Fix 4: Verify key has Calendar API access
```

### Weather Returns Error
```
Issue: "Could not find weather for [city]"
Fix 1: Check city name spelling
Fix 2: Verify API key is correct
Fix 3: Check OpenWeather API status: https://status.openweathermap.org/
```

### Calendar Not Syncing
```
Issue: "Google Calendar not configured"
Fix 1: Ensure credentials.json is in project root
Fix 2: Delete credentials.json and re-authenticate
Fix 3: Check internet connection
Fix 4: Verify calendar permissions are granted
```

---

## 9. Advanced: Custom API Integration

### Adding a New API Service

Example: Adding a custom news API

```python
# engine/news_module.py
import requests
import eel
from engine.command import speak

NEWS_API_KEY = None
NEWS_API_ENDPOINT = "https://newsapi.org/v2/top-headlines"

def set_news_api_key(api_key):
    global NEWS_API_KEY
    NEWS_API_KEY = api_key

@eel.expose
def get_news(category="general", country="us"):
    """Get top news headlines"""
    try:
        params = {
            'category': category,
            'country': country,
            'apiKey': NEWS_API_KEY
        }
        
        response = requests.get(NEWS_API_ENDPOINT, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            articles = data['articles'][:5]
            
            message = f"Here are the top {category} news headlines: "
            for article in articles:
                message += article['title'] + ". "
            
            speak(message)
            return articles
        
        speak("Error getting news")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None
```

Then add to command.py:
```python
elif 'news' in query:
    from engine.news_module import get_news
    get_news()
```

---

## 10. Security Best Practices

1. **Never commit API keys to Git**
   ```bash
   # Add to .gitignore
   echo "engine/config.py" >> .gitignore
   echo ".env" >> .gitignore
   ```

2. **Use environment variables**
   - More secure than hardcoded keys

3. **Restrict API key permissions**
   - Only enable needed APIs
   - Set usage limits

4. **Rotate keys regularly**
   - Generate new keys monthly
   - Delete old keys after rotation

5. **Monitor usage**
   - Check API dashboard regularly
   - Set up billing alerts

---


For questions or issues with API setup, refer to official documentation or create an issue in the project repository.
