"""
Contact Management Module
Manages local contacts with voice command support for add, list, and delete operations
"""

import sqlite3
import eel
from engine.command import speak
import re

# Initialize contact database
CONTACTS_DB = 'contacts.db'

def init_contacts_db():
    """Initialize contacts database"""
    conn = sqlite3.connect(CONTACTS_DB)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        phone TEXT NOT NULL,
        email TEXT,
        created_at TEXT NOT NULL
    )
    """)
    
    conn.commit()
    conn.close()

# Initialize on module load
init_contacts_db()

@eel.expose
def add_contact_voice(query):
    """
    Add a contact via voice command
    Expected format: "add contact name as phone number [email]"
    Example: "add contact mom as plus one nine one nine nine nine nine nine nine nine nine"
    """
    try:
        query = query.lower()
        
        # Extract phone number from various formats
        phone_match = re.search(r'plus\s+(\d+(?:\s+\d+)*)', query)
        if phone_match:
            phone = phone_match.group(1).replace(' ', '')
        else:
            phone_match = re.search(r'(\d{7,15})', query)
            if phone_match:
                phone = phone_match.group(1)
            else:
                speak("Please provide a valid phone number")
                return False
        
        # Extract name
        name_match = re.search(r'contact\s+([a-z\s]+?)\s+(?:as|to|at)', query)
        if name_match:
            name = name_match.group(1).strip()
        else:
            speak("Please provide a contact name")
            return False
        
        # Extract email if provided
        email_match = re.search(r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', query)
        email = email_match.group(1) if email_match else None
        
        # Add to database
        conn = sqlite3.connect(CONTACTS_DB)
        cursor = conn.cursor()
        
        try:
            import datetime
            cursor.execute(
                "INSERT INTO contacts (name, phone, email, created_at) VALUES (?, ?, ?, ?)",
                (name, phone, email, datetime.datetime.now().isoformat())
            )
            conn.commit()
            speak(f"Contact {name} added successfully with phone number {phone}")
            eel.DisplayMessage(f"Contact {name} added: {phone}")
            return True
        except sqlite3.IntegrityError:
            speak(f"Contact {name} already exists")
            return False
        finally:
            conn.close()
            
    except Exception as e:
        print(f"Error adding contact: {e}")
        speak("Error adding contact")
        return False

@eel.expose
def list_contacts_voice():
    """List all contacts via voice"""
    try:
        conn = sqlite3.connect(CONTACTS_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT name, phone FROM contacts ORDER BY name")
        contacts = cursor.fetchall()
        conn.close()
        
        if not contacts:
            speak("You have no contacts")
            return []
        
        contact_list = []
        message = f"You have {len(contacts)} contacts: "
        
        for name, phone in contacts:
            contact_list.append({'name': name, 'phone': phone})
            message += f"{name}, "
        
        speak(message.rstrip(', '))
        return contact_list
        
    except Exception as e:
        print(f"Error listing contacts: {e}")
        speak("Error retrieving contacts")
        return []

@eel.expose
def delete_contact_voice(query):
    """
    Delete a contact via voice command
    Expected format: "delete contact [name]"
    """
    try:
        query = query.lower()
        
        # Extract contact name
        name_match = re.search(r'delete\s+contact\s+([a-z\s]+)', query)
        if not name_match:
            speak("Please provide a contact name to delete")
            return False
        
        name = name_match.group(1).strip()
        
        conn = sqlite3.connect(CONTACTS_DB)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM contacts WHERE LOWER(name) = ?", (name.lower(),))
        conn.commit()
        
        if cursor.rowcount > 0:
            speak(f"Contact {name} deleted successfully")
            return True
        else:
            speak(f"Contact {name} not found")
            return False
            
    except Exception as e:
        print(f"Error deleting contact: {e}")
        speak("Error deleting contact")
        return False

@eel.expose
def search_contact(name):
    """Search for a contact by name"""
    try:
        conn = sqlite3.connect(CONTACTS_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT name, phone, email FROM contacts WHERE LOWER(name) LIKE ?", 
                      (f"%{name.lower()}%",))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {'name': result[0], 'phone': result[1], 'email': result[2]}
        return None
        
    except Exception as e:
        print(f"Error searching contact: {e}")
        return None

@eel.expose
def get_contact_phone(name):
    """Get phone number for a contact"""
    try:
        conn = sqlite3.connect(CONTACTS_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT phone FROM contacts WHERE LOWER(name) = ?", (name.lower(),))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0]
        return None
        
    except Exception as e:
        print(f"Error getting contact phone: {e}")
        return None
