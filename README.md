# Sophia AI Assistant Commands

Use these commands by typing in Sophia or speaking into the microphone.

## Run Sophia

```powershell
cd .\sophia-AI-main
.\envSophia\Scripts\python.exe .\Sophia-AI-Assistant-master\main.py
```

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
add contact mom as 919999999999
add contact rahul as 918888888888
list contacts
show contacts
delete contact mom
```

## WhatsApp And Messaging

```text
send whatsapp message to +919999999999 hello
send whatsapp message to mom hello
send telegram message to @username hello
chat hello to @username
```

## Video Calls

```text
video call whatsapp to +919999999999
video call whatsapp to mom
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



## API Keys

Set API keys in PowerShell before running Sophia:

```powershell
$env:GOOGLE_API_KEY="your_gemini_key"
$env:HF_API_TOKEN="your_huggingface_token"
$env:OPENWEATHER_API_KEY="your_openweather_key"
```

Then run:

```powershell
..\envSophia\Scripts\python.exe main.py
```
