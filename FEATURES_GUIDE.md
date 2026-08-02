# Sophia AI Assistant - Complete Feature Guide

## Overview
Sophia is an advanced voice-controlled AI assistant with multiple integrated features including face recognition, contact management, conversational AI, weather updates, calendar integration, and more.

## New Features Added

### 1. **Intelligent Face Recognition** 
Real-time face recognition for personalized greetings and user-specific activation.

**Features:**
- Register multiple users' faces
- Automatic user recognition on startup
- Personalized greetings based on recognized user
- Uses LBPH (Local Binary Patterns Histograms) face recognizer

**Voice Commands:**
- "Recognize me" - Recognize current user from webcam
- "Register face" - Register a new user's face
- "Register my face" - Register your own face

**Setup:**
```bash
# Face recognition uses OpenCV, already included in requirements
# No additional setup needed
```

---

### 2. **Voice-Controlled Contact Management** 
Manage local contacts with full voice command support.

**Features:**
- Add contacts via voice
- List all contacts
- Delete contacts
- Search contacts
- Integration with WhatsApp messaging

**Voice Commands:**
- "Add contact mom as plus one nine one nine nine nine nine nine nine nine" - Add a contact
- "List contacts" / "Show contacts" - View all contacts
- "Delete contact mom" - Delete a contact

**Database:**
- Contacts are stored in `contacts.db` SQLite database
- Supports: name, phone number, email, creation timestamp

---

### 3. **Conversational AI Integration** 
Powered by Google Gemini API and Hugging Face API for intelligent conversations.

**Features:**
- Ask questions and get intelligent answers
- General knowledge queries
- Natural conversation support
- Conversation history tracking
- Fallback between multiple AI services

**Voice Commands:**
- "What is the capital of France?" - Ask questions
- "Tell me about quantum physics"
- "How do I make pasta?"

**Setup:**

#### Google Gemini API:
1. Visit https://ai.google.dev/
2. Click "Get API Key"
3. Create a new API key
4. Add to `engine/config.py`:
```python
GEMINI_API_KEY = "your_api_key_here"
```

#### Hugging Face API:
1. Visit https://huggingface.co/settings/tokens
2. Create a new token
3. Add to `engine/config.py`:
```python
HUGGINGFACE_API_TOKEN = "your_token_here"
```

---

### 4. **Information Retrieval System** 
Fetch information from multiple sources including Wikipedia, weather, and calendar.

**Features:**
- Wikipedia summaries for any topic
- Real-time weather updates
- Weather forecasts
- Google Calendar integration
- Information search

**Voice Commands:**
- "What is artificial intelligence?" - Wikipedia search
- "Weather in New York" - Current weather
- "Weather forecast" - 5-day forecast
- "Show my calendar" / "My events" - Calendar events

**Setup:**

#### OpenWeather API:
1. Visit https://openweathermap.org/api
2. Sign up for free tier
3. Get your API key
4. Add to `engine/config.py`:
```python
WEATHER_API_KEY = "your_api_key_here"
```

#### Google Calendar API:
1. Go to https://developers.google.com/calendar/api
2. Enable the Calendar API
3. Create OAuth 2.0 credentials (Desktop application)
4. Download credentials JSON file
5. Place in project root as `credentials.json`
6. First run will prompt you to authenticate

---

### 5. **Advanced Contact & WhatsApp Integration**
Enhanced WhatsApp messaging with saved contacts.

**Features:**
- Send WhatsApp messages using contact names
- Send messages to phone numbers
- Video calling support
- Support for WhatsApp, Telegram, and Facebook

**Voice Commands:**
- "Send WhatsApp message to mom hello" - Send to contact
- "Send WhatsApp to plus 1 234 567 8900 hello" - Send to number
- "Video call on WhatsApp to mom" - Start video call

**Usage:**
- First add contacts using the contact management feature
- Then reference them by name in messaging commands

---

## Installation & Setup

### 1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Configure API Keys**
Edit `engine/config.py` and add your API keys:
```python
GEMINI_API_KEY = "your_key_here"
HUGGINGFACE_API_TOKEN = "your_token_here"
WEATHER_API_KEY = "your_key_here"
```

### 3. **Setup Google Calendar (Optional)**
1. Place `credentials.json` in project root
2. Run the application and authenticate when prompted

### 4. **Initialize Databases**
The following databases are created automatically on first run:
- `sophia.db` - Reminders and system database
- `contacts.db` - Contact management database
- `face_database.pkl` - Face recognition data

---

## Directory Structure

```
Sophia-AI-Assistant/
├── engine/
│   ├── command.py              # Voice command processing
│   ├── features.py             # Core features
│   ├── config.py               # Configuration & API keys
│   ├── db.py                   # Database management
│   ├── chat.py                 # Chat functionality
│   ├── face_recognition_module.py   # NEW: Face recognition
│   ├── contact_manager.py            # NEW: Contact management
│   ├── ai_conversation.py            # NEW: AI conversations
│   └── info_retrieval.py             # NEW: Information retrieval
├── www/
│   ├── index.html
│   ├── main.js
│   ├── controller.js
│   └── assets/
├── main.py                     # Main application
├── requirements.txt            # Dependencies
├── sophia.db                   # Auto-created: Reminders DB
├── contacts.db                 # Auto-created: Contacts DB
└── credentials.json            # Google Calendar credentials (optional)
```

---

## Usage Examples

### Example 1: Add Contact and Send Message
```
User: "Add contact Sarah as plus one two one two five five five one two one two"
Sophia: "Contact Sarah added successfully"

User: "Send WhatsApp message to Sarah hello how are you"
Sophia: "Opening WhatsApp chat"
```

### Example 2: Face Recognition Activation
```
User: "Register face"
Sophia: "Please tell me your name"
User: "John"
Sophia: "Starting face registration... Look at the camera"
[30 sample photos are taken]
Sophia: "Face registration complete for John"

User: "Recognize me"
Sophia: "Welcome back, John!"
```

### Example 3: Weather and Information
```
User: "Weather in London"
Sophia: "In London, it's 15°C and mostly cloudy..."

User: "What is machine learning?"
Sophia: "Machine learning is a subset of artificial intelligence..."
```

### Example 4: AI Conversation
```
User: "How do I learn Python?"
Sophia: "Here are some great ways to learn Python..."

User: "Tell me a joke"
Sophia: "Why did the programmer quit his job?..."
```

---

## Voice Command Reference

### Face Recognition
- "Recognize me"
- "Register face"
- "Register my face"

### Contact Management
- "Add contact [name] as [phone]"
- "List contacts" / "Show contacts"
- "Delete contact [name]"

### Messaging
- "Send WhatsApp message to [contact/number] [message]"
- "Send Telegram message to [@username] [message]"
- "Video call on WhatsApp to [contact]"

### Information
- "What is [topic]?"
- "Weather in [city]"
- "Weather forecast"
- "Calendar" / "My events" / "Show schedule"

### AI Conversation
- "Ask [question]"
- "Tell me about [topic]"
- "How [question]?"

### Existing Commands
- "Open [app]" - Open applications
- "Play [song] on YouTube"
- "Remind me to [task]"
- "List reminders"

---

## Troubleshooting

### Face Recognition Issues
- **Issue**: Camera not detected
  - **Solution**: Check webcam is connected and not in use by another app
  
- **Issue**: Poor recognition accuracy
  - **Solution**: Register more samples, ensure good lighting, register from different angles

### API Connection Issues
- **Issue**: "API key not configured"
  - **Solution**: Check you added the key to `engine/config.py`
  
- **Issue**: Timeout errors
  - **Solution**: Check internet connection and API quota limits

### Database Issues
- **Issue**: Contact not found when trying to message
  - **Solution**: Verify contact name spelling, re-add the contact

---

## Performance Tips

1. **Face Recognition**: Register 30-50 samples per user for best accuracy
2. **Weather API**: Calls are rate-limited, cache results if possible
3. **AI Responses**: Longer queries may take 5-10 seconds, be patient
4. **Contacts**: Use unique, clear contact names for voice recognition

---

## Future Enhancements

Potential features to add:
- Email integration and sending
- Expense tracking
- Task management and to-do lists
- News and RSS feed integration
- Smart home device control
- Improved speech recognition accuracy
- Multi-language support
- Mobile app companion
- Cloud backup of contacts and settings

---

## License

This project uses multiple open-source libraries. See individual library licenses for details.

---

## Support

For issues or questions:
1. Check the Troubleshooting section
2. Review API documentation for your chosen services
3. Check console logs for detailed error messages
4. Verify all dependencies are installed: `pip install -r requirements.txt`

---

**Enjoy using Sophia! **
