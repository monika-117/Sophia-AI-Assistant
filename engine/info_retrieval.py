"""
Information Retrieval Module
Fetch Wikipedia summaries, check real-time weather updates, and access Google Calendar events
"""

import requests
import eel
from engine.command import speak
import re
from datetime import datetime, timedelta

# API Keys and endpoints
WEATHER_API_KEY = None
WEATHER_API_ENDPOINT = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_API_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
WIKIPEDIA_API_ENDPOINT = "https://en.wikipedia.org/w/api.php"
WIKIPEDIA_HEADERS = {
    "User-Agent": "SophiaAIAssistant/1.0 (local desktop assistant; contact: local-user)"
}

def set_weather_api_key(api_key):
    """Set OpenWeather API key"""
    global WEATHER_API_KEY
    WEATHER_API_KEY = api_key

def set_calendar_service(service):
    """Calendar integration removed — no-op stub to preserve imports."""
    # Intentionally do nothing. Calendar features removed on user request.
    return None

class InformationRetriever:
    """Handle information retrieval from various sources"""
    
    @eel.expose
    def get_wikipedia_summary(self, topic):
        """
        Get Wikipedia summary for a topic
        """
        topic = clean_wikipedia_topic(topic)
        if not topic:
            speak("Please tell me what to search on Wikipedia.")
            return None

        try:
            page_title = self.find_wikipedia_title(topic)
            if not page_title:
                speak(f"No information found about {topic}")
                return None

            extract = self.fetch_wikipedia_extract(page_title)
            if not extract:
                speak(f"No summary found for {page_title}")
                return None

            summary = extract[:500] + "..." if len(extract) > 500 else extract
            speak(summary)
            return summary
        except requests.exceptions.Timeout:
            speak("Wikipedia request timed out")
            return None
        except Exception as e:
            print(f"Error getting Wikipedia summary: {e}")
            speak("Error retrieving information")
            return None

    def find_wikipedia_title(self, topic):
        """Find the best Wikipedia page title for natural search text."""
        params = {
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'srsearch': topic,
            'srlimit': 1,
        }
        response = requests.get(WIKIPEDIA_API_ENDPOINT, params=params, headers=WIKIPEDIA_HEADERS, timeout=10)
        response.raise_for_status()
        results = response.json().get('query', {}).get('search', [])
        if results:
            return results[0].get('title')
        return None

    def fetch_wikipedia_extract(self, title):
        """Fetch the intro summary for a resolved Wikipedia title."""
        params = {
            'action': 'query',
            'format': 'json',
            'titles': title,
            'prop': 'extracts',
            'explaintext': True,
            'exintro': True,
            'redirects': 1,
        }
        response = requests.get(WIKIPEDIA_API_ENDPOINT, params=params, headers=WIKIPEDIA_HEADERS, timeout=10)
        response.raise_for_status()
        pages = response.json().get('query', {}).get('pages', {})
        for page_data in pages.values():
            extract = page_data.get('extract')
            if extract:
                return extract
        return None
    
    @eel.expose
    def get_weather(self, city, units='metric'):
        """
        Get current weather for a city
        units: 'metric' (Celsius) or 'imperial' (Fahrenheit)
        """
        try:
            if not WEATHER_API_KEY:
                return self.get_weather_from_wttr(city)
            
            params = {
                'q': city,
                'appid': WEATHER_API_KEY,
                'units': units
            }
            
            response = requests.get(WEATHER_API_ENDPOINT, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                city_name = data['name']
                temp = data['main']['temp']
                feels_like = data['main']['feels_like']
                humidity = data['main']['humidity']
                description = data['weather'][0]['description']
                wind_speed = data['wind']['speed']
                
                unit_symbol = '°C' if units == 'metric' else '°F'
                weather_message = f"In {city_name}, it's {temp}{unit_symbol} and {description}. Feels like {feels_like}{unit_symbol}. Humidity is {humidity}%. Wind speed is {wind_speed} meters per second."
                
                speak(weather_message)
                return {
                    'city': city_name,
                    'temperature': temp,
                    'feels_like': feels_like,
                    'humidity': humidity,
                    'description': description,
                    'wind_speed': wind_speed
                }
            
            speak(f"Could not find weather for {city}")
            return None
            
        except requests.exceptions.Timeout:
            speak("Weather request timed out")
            return None
        except Exception as e:
            print(f"Error getting weather: {e}")
            speak("Error retrieving weather")
            return None

    def get_weather_from_wttr(self, city):
        """Fallback weather lookup that does not require an API key."""
        try:
            response = requests.get(f"https://wttr.in/{city}", params={"format": "j1"}, timeout=10)
            response.raise_for_status()
            data = response.json()
            current = data["current_condition"][0]
            area = data.get("nearest_area", [{}])[0]
            city_name = area.get("areaName", [{}])[0].get("value", city)
            description = current.get("weatherDesc", [{}])[0].get("value", "current conditions")
            temp = current.get("temp_C")
            feels_like = current.get("FeelsLikeC")
            humidity = current.get("humidity")
            wind_speed = current.get("windspeedKmph")
            weather_message = (
                f"In {city_name}, it's {temp} degrees Celsius and {description}. "
                f"Feels like {feels_like} degrees. Humidity is {humidity}%. "
                f"Wind speed is {wind_speed} kilometers per hour."
            )
            speak(weather_message)
            return {
                "city": city_name,
                "temperature": temp,
                "feels_like": feels_like,
                "humidity": humidity,
                "description": description,
                "wind_speed": wind_speed,
            }
        except Exception as e:
            print(f"Error getting fallback weather: {e}")
            speak("Weather lookup is not available right now.")
            return None
    
    @eel.expose
    def get_weather_forecast(self, city, days=1, units='metric'):
        """
        Get weather forecast for a city
        """
        try:
            if not WEATHER_API_KEY:
                return self.get_weather_from_wttr(city)
            
            params = {
                'q': city,
                'appid': WEATHER_API_KEY,
                'units': units
            }
            
            response = requests.get(FORECAST_API_ENDPOINT, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                forecasts = []
                
                # Get forecast for every 24 hours
                for i in range(0, min(len(data['list']), days * 8), 8):
                    forecast_data = data['list'][i]
                    forecast = {
                        'datetime': forecast_data['dt_txt'],
                        'temp': forecast_data['main']['temp'],
                        'description': forecast_data['weather'][0]['description'],
                        'humidity': forecast_data['main']['humidity']
                    }
                    forecasts.append(forecast)
                
                # Build voice message
                message = f"Weather forecast for {city}: "
                for forecast in forecasts[:3]:
                    message += f"{forecast['datetime']}: {forecast['temp']}°C and {forecast['description']}. "
                
                speak(message)
                return forecasts
            
            speak(f"Could not get forecast for {city}")
            return None
            
        except Exception as e:
            print(f"Error getting weather forecast: {e}")
            speak("Error retrieving forecast")
            return None
    
    # Calendar functions removed. get_calendar_events was intentionally deleted.
    
    @eel.expose
    def search_info(self, query):
        """
        Search for general information using Wikipedia
        """
        return self.get_wikipedia_summary(query)

# Global information retriever
info_retriever = InformationRetriever()

@eel.expose
def fetch_wikipedia(topic):
    """Get Wikipedia summary"""
    return info_retriever.get_wikipedia_summary(topic)


def clean_wikipedia_topic(query):
    """Convert voice-style commands into a clean Wikipedia search topic."""
    topic = (query or "").lower().strip()
    replacements = [
        "wikipedia",
        "search for",
        "search",
        "what is",
        "who is",
        "tell me about",
        "tell me",
    ]
    for phrase in replacements:
        topic = re.sub(r'\b' + re.escape(phrase) + r'\b', '', topic)
    return re.sub(r'\s+', ' ', topic).strip(" ?.")

@eel.expose
def check_weather(city):
    """Check current weather"""
    return info_retriever.get_weather(city)

@eel.expose
def check_weather_forecast(city, days=1):
    """Check weather forecast"""
    return info_retriever.get_weather_forecast(city, days)

@eel.expose
def get_calendar():
    """Calendar feature removed — returns None and speaks a notice."""
    speak('Calendar feature has been removed')
    return None

@eel.expose
def search_information(query):
    """Search for information"""
    return info_retriever.search_info(query)
