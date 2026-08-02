# Sophia AI Assistant Commands

Use these commands by typing in Sophia or speaking into the microphone.

## Run Sophia

```powershell
cd .\sophia-AI-main
.\envSophia\Scripts\python.exe .\Sophia-AI-Assistant-master\main.py
```

# Sophia AI Assistant
Sophia is a desktop AI assistant built using Python that can perform various tasks such as answering questions like ChatGPT, opening desktop applications, browsing websites, and even making phone and WhatsApp calls. This project is designed to be versatile and extensible, with the ability to add more functionalities easily. It integrates the Hugging Face API, a free ChatGPT alternative to simulate conversation, and offers multiple activation methods for user commands.

## output
![image alt](https://github.com/monika-117/sophia-AI/blob/d703342b2a4f4ccfb0627d949dc04c920e618e72/output.png)


## Features

* **Voice Activation:** Activate Sophia by saying "Sophia."
* **Text Input:** Type your queries and press enter to receive a response.
* **App Control:** Open applications like Notepad and OneNote.
* **Website Navigation:** Open websites like YouTube and Canva.
* **Multimedia Control:** Search and play specific videos on YouTube.
* **Phone and WhatsApp Communication:** Make calls or send messages.

## Enabling Chat Responses (ChatGPT-like)

This assistant can answer questions in a conversational way using the Hugging Face Inference API. To enable full ChatGPT-like responses:

1. Get a Hugging Face API token from https://huggingface.co/settings/tokens and set it in your environment:

   - Windows PowerShell:

     ```powershell
     $env:HF_API_TOKEN = "hf_xxx"
     ```

   - Or permanently via System Environment Variables.

2. (Optional) Choose a model by setting `HF_MODEL` environment variable (default: `google/flan-t5-large`).

3. Restart the app. Typed questions or voice queries that are not recognized as commands will be sent to the Hugging Face Inference API and Sophia will speak and display the response.

If no token is provided, the assistant will show a message explaining how to enable chat responses.


## Technology Used:
- #### Languages:
  - ![PYTHON](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=darkgreen)
  - ![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
  - ![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
  - ![JAVASCRIPT](https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E)
- #### FrameWork:
  - ![BOOTSTRAP](https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white)
- #### Database:
  - ![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
- #### API used for:
  - Hugging Face API ![Hugging Face API](https://github.com/user-attachments/assets/17108a47-2fbf-4ea7-bac7-b66e3fafe9e0)

## Installation

### Prerequisites
Make sure you have Python installed. Then, install the following packages:

```bash
beautifulsoup4==4.12.3
blinker==1.8.2
bottle @ git+https://github.com/bottlepy/bottle.git@3fdb8b2a2e0d1641374b53ef2b051fe7f54508b5
bottle-websocket==0.2.9
certifi==2024.7.4
cffi==1.16.0
charset-normalizer==3.3.2
click==8.1.7
colorama==0.4.6
comtypes==1.4.4
Eel==0.16.0
enum34==1.1.10
Flask==3.0.3
future==1.0.0
gevent==24.2.1
gevent-websocket==0.10.1
greenlet==3.0.3
hugchat==0.4.8
idna==3.7
itsdangerous==2.2.0
Jinja2==3.1.4
MarkupSafe==2.1.5
MouseInfo==0.1.3
numpy==2.0.0
pillow==10.4.0
playsound==1.2.2
pocketsphinx==5.0.3
psutil==6.0.0
pvporcupine==1.9.5
PyAudio==0.2.14
PyAutoGUI==0.9.54
pycparser==2.22
PyGetWindow==0.0.9
PyMsgBox==1.0.9
pyparsing==3.1.2
pyperclip==1.9.0
pypiwin32==223
PyRect==0.2.0
PyScreeze==0.1.30
pyttsx3==2.90
pytweening==1.2.0
pywhatkit==5.4
pywin32==306
requests==2.32.3
requests-toolbelt==1.0.0
setuptools==70.2.0
sounddevice==0.4.7
soupsieve==2.5
SpeechRecognition==3.10.4
typing_extensions==4.12.2
urllib3==2.2.2
Werkzeug==3.0.3
whichcraft==0.6.1
wikipedia==1.4.0
zope.event==5.0
zope.interface==6.4.post2
```

### Setup Instructions

**Clone the Repository:**
   ```bash
   git clone https://github.com/monika-117/sophia-AI.git
   cd sophia-AI
```
__To install the necessary dependencies and set up the API and database,please contact @monika-117__


## Usage

### Activating the Assistant
There are several ways to activate Sophia:

- **Voice Activation:** Simply say "Sophia."
- **Text Input:** Type your query in the input box (e.g., "How are you?").
- **Keyboard Shortcut:** Press `Window + J` to activate the assistant.

### Supported Commands

#### Query Answering
Ask Sophia questions, and she'll answer using the Hugging Face API, a free ChatGPT alternative.
**Example:** "Tell me about yourself"


## Open Apps And Websites

```text
open notepad
open chrome
open calculator
open vscode
open file manager
open command prompt
open youtube
open github
open instagram
open facebook
open canva
open whatsapp
open telegram
```

## YouTube

```text
play shape of you on youtube
play python tutorial on youtube
open youtube search for ai assistant project
```

## Wikipedia And Information

```text
who is Ada Lovelace
what is artificial intelligence
search Python programming
wikipedia machine learning
```

## Conversational AI

```text
tell me a joke
ask what is machine learning
how does photosynthesis work
why is the sky blue
tell me about computers
ask explain python in simple words
```

## Weather

```text
weather in Delhi
weather in Mumbai
weather forecast in Bangalore
```

## Reminders

```text
remind me to drink water at 6 pm
remind me in 10 minutes to check the oven
list reminders
show reminders
```

## Contacts

```text
add contact username as 919999999999
add contact rahul as 918888888888
list contacts
show contacts
delete contact username 
```

## WhatsApp And Messaging

```text
send whatsapp message to +919999999999 hello
send whatsapp message to user hello
send telegram message to @username hello
chat hello to @username
```

## Video Calls

```text
video call whatsapp to +919999999999
video call whatsapp to @username 
video call telegram to @username
video call facebook to friend_name
```

Note: WhatsApp does not provide a direct public link that starts a video call. Sophia opens the chat and tries to click the video-call button automatically.

## Face Recognition

```text
register my face
recognize me
face recognition
```

## Calendar

```text
calendar
my events
schedule
```

Calendar requires Google Calendar credentials. If it is not configured, Sophia will say Google Calendar is not configured.

## API Keys

Set API keys in PowerShell before running Sophia:

```powershell
$env:GOOGLE_API_KEY="your_gemini_key"
$env:HF_API_TOKEN="your_huggingface_token"
$env:OPENWEATHER_API_KEY="your_openweather_key"
```


Notes:
- Phone numbers should include the country code when possible (e.g., `+123456789`).
- Telegram usernames may be given with or without the `@` prefix.
- Messaging and calling flows open the web clients (WhatsApp Web / Telegram Web / Messenger); you must be logged in to complete send/call actions.



## Contributing
Feel free to open issues or submit pull requests to improve the project. Contributions are welcome, whether it’s adding new features, fixing bugs, or improving documentation.


