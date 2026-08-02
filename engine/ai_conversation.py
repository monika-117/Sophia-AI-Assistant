"""
Conversational AI Module
Integrated with Google Gemini API and Hugging Face API for dynamic question-answering
and natural conversation
"""

import requests
import eel
from engine.command import speak
import re

# API endpoints and models
GEMINI_API_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
HF_API_ENDPOINT = "https://api-inference.huggingface.co/models"

# You'll need to set these in config.py
GEMINI_API_KEY = None
HF_API_TOKEN = None

def set_api_keys(gemini_key, hf_token):
    """Set API keys for external services"""
    global GEMINI_API_KEY, HF_API_TOKEN
    GEMINI_API_KEY = gemini_key
    HF_API_TOKEN = hf_token

class ConversationalAI:
    """Handle conversational AI interactions"""
    
    def __init__(self):
        self.conversation_history = []
        self.max_history = 10
    
    @eel.expose
    def ask_gemini(self, question):
        """
        Ask a question using Google Gemini API
        """
        try:
            if not GEMINI_API_KEY:
                return self.local_fallback(question)
            
            headers = {
                "Content-Type": "application/json",
            }
            
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": question
                            }
                        ]
                    }
                ]
            }
            
            url = f"{GEMINI_API_ENDPOINT}?key={GEMINI_API_KEY}"
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    answer = result['candidates'][0]['content']['parts'][0]['text']
                    self.conversation_history.append({
                        'question': question,
                        'answer': answer,
                        'source': 'gemini'
                    })
                    
                    # Keep conversation history limited
                    if len(self.conversation_history) > self.max_history:
                        self.conversation_history.pop(0)
                    
                    speak(answer)
                    return answer
            
            return self.local_fallback(question)
            
        except requests.exceptions.Timeout:
            return self.local_fallback(question)
        except Exception as e:
            print(f"Error querying Gemini: {e}")
            return self.local_fallback(question)
    
    @eel.expose
    def ask_huggingface(self, question, model="gpt2"):
        """
        Ask a question using Hugging Face API
        Default model: gpt2
        Other options: text-davinci-003, distilgpt2, etc.
        """
        try:
            if not HF_API_TOKEN:
                return self.local_fallback(question)
            
            headers = {
                "Authorization": f"Bearer {HF_API_TOKEN}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "inputs": question,
                "parameters": {
                    "max_length": 100,
                    "temperature": 0.7
                }
            }
            
            url = f"{HF_API_ENDPOINT}/{model}"
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    if 'generated_text' in result[0]:
                        answer = result[0]['generated_text']
                    else:
                        answer = str(result[0])
                    
                    self.conversation_history.append({
                        'question': question,
                        'answer': answer,
                        'source': 'huggingface'
                    })
                    
                    speak(answer)
                    return answer
            
            return self.local_fallback(question)
            
        except requests.exceptions.Timeout:
            return self.local_fallback(question)
        except Exception as e:
            print(f"Error querying Hugging Face: {e}")
            return self.local_fallback(question)
    
    @eel.expose
    def chat(self, question, preferred_service="gemini"):
        """
        Smart chat function that picks the best available service.
        """
        if self.has_direct_local_answer(question):
            return self.local_fallback(question)
        if preferred_service == "huggingface" and HF_API_TOKEN:
            return self.ask_huggingface(question)
        if preferred_service == "gemini" and GEMINI_API_KEY:
            return self.ask_gemini(question)
        if HF_API_TOKEN:
            return self.ask_huggingface(question)
        return self.local_fallback(question)

    def has_direct_local_answer(self, question):
        """Use local answers for known prompts instead of trying cloud APIs first."""
        q = question.lower()
        return any(
            phrase in q
            for phrase in [
                "joke",
                "machine learning",
                "photosynthesis",
                "sky blue",
                "blue sky",
            ]
        )

    def local_fallback(self, question):
        """Answer locally when cloud AI keys are missing or unavailable."""
        try:
            from engine.chat import get_chat_response
            answer = get_chat_response(question)
        except Exception as e:
            print(f"Local chat fallback failed: {e}")
            answer = "I could not answer that right now."

        self.conversation_history.append({
            'question': question,
            'answer': answer,
            'source': 'local'
        })
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)
        speak(answer)
        return answer
    
    @eel.expose
    def get_conversation_history(self):
        """Return conversation history"""
        return self.conversation_history
    
    @eel.expose
    def clear_conversation_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        speak("Conversation history cleared")
        return True

# Global AI instance
ai_engine = ConversationalAI()

@eel.expose
def ask_question(question, service="gemini"):
    """Main entry point for asking questions"""
    return ai_engine.chat(question, service)

@eel.expose
def general_knowledge_query(query):
    """Query for general knowledge using AI"""
    return ai_engine.ask_gemini(f"Provide a concise answer about: {query}")

@eel.expose
def natural_conversation(statement):
    """Have a natural conversation"""
    return ai_engine.ask_gemini(f"Respond naturally to: {statement}")
