"""
Face Recognition Module for Intelligent Activation
Provides real-time face recognition for personalized greetings and user-specific activation
"""

import cv2
import numpy as np
import os
import pickle
import eel
from pathlib import Path
from engine.command import speak
import datetime

# Configuration
FACE_CASCADE_PATH = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
try:
    FACE_RECOGNIZER = cv2.face.LBPHFaceRecognizer_create()
except Exception:
    FACE_RECOGNIZER = None
KNOWN_FACES_DIR = 'known_faces'
FACE_DATABASE_FILE = 'face_database.pkl'

# Load or create face cascade
try:
    face_cascade = cv2.CascadeClassifier(FACE_CASCADE_PATH)
except Exception as e:
    print(f"Error loading face cascade: {e}")
    face_cascade = None

# Create known_faces directory if it doesn't exist
if not os.path.exists(KNOWN_FACES_DIR):
    os.makedirs(KNOWN_FACES_DIR)

class FaceRecognitionManager:
    """Manages face recognition and user identification"""
    
    def __init__(self):
        self.trained = False
        self.user_labels = {}
        self.load_face_database()
        
    def load_face_database(self):
        """Load face database from pickle file"""
        try:
            if os.path.exists(FACE_DATABASE_FILE):
                with open(FACE_DATABASE_FILE, 'rb') as f:
                    self.user_labels = pickle.load(f)
            else:
                self.user_labels = {}
        except Exception as e:
            print(f"Error loading face database: {e}")
            self.user_labels = {}
    
    def save_face_database(self):
        """Save face database to pickle file"""
        try:
            with open(FACE_DATABASE_FILE, 'wb') as f:
                pickle.dump(self.user_labels, f)
        except Exception as e:
            print(f"Error saving face database: {e}")
    
    @eel.expose
    def register_face(self, user_name, num_samples=30):
        """
        Register a new user's face
        Args:
            user_name: Name of the user
            num_samples: Number of samples to capture (default 30)
        """
        try:
            if face_cascade is None:
                speak("Face detection is not available on this installation.")
                return False
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                speak("Cannot access webcam")
                return False
            
            user_dir = os.path.join(KNOWN_FACES_DIR, user_name)
            if not os.path.exists(user_dir):
                os.makedirs(user_dir)
            
            speak(f"Starting face registration for {user_name}. Look at the camera.")
            count = 0
            
            while count < num_samples:
                ret, frame = cap.read()
                if not ret:
                    break
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    face_roi = frame[y:y+h, x:x+w]
                    cv2.imwrite(f"{user_dir}/{count}.jpg", face_roi)
                    count += 1
                
                cv2.imshow('Face Registration - Press Q to quit', frame)
                
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            
            if count > 0:
                self.user_labels[user_name] = {
                    'samples': count,
                    'registered_at': datetime.datetime.now().isoformat()
                }
                self.save_face_database()
                speak(f"Face registration complete for {user_name} with {count} samples")
                return True
            else:
                speak("No faces detected during registration")
                return False
                
        except Exception as e:
            print(f"Error during face registration: {e}")
            speak("Error during face registration")
            return False
    
    def train_face_recognizer(self):
        """Train the face recognizer with all registered faces"""
        try:
            if FACE_RECOGNIZER is None:
                speak("Face recognition needs opencv-contrib-python. Please install it and try again.")
                return False
            faces = []
            labels = []
            label_id = 0
            label_map = {}
            
            for user_name in os.listdir(KNOWN_FACES_DIR):
                user_dir = os.path.join(KNOWN_FACES_DIR, user_name)
                if not os.path.isdir(user_dir):
                    continue
                
                label_map[label_id] = user_name
                
                for img_name in os.listdir(user_dir):
                    img_path = os.path.join(user_dir, img_name)
                    img = cv2.imread(img_path)
                    if img is None:
                        continue
                    
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    face_roi = cv2.resize(gray, (200, 200))
                    faces.append(face_roi)
                    labels.append(label_id)
                
                label_id += 1
            
            if len(faces) > 0:
                FACE_RECOGNIZER.train(faces, np.array(labels))
                self.trained = True
                self.label_map = label_map
                speak("Face recognizer trained successfully")
                return True
            else:
                speak("No faces found for training")
                return False
                
        except Exception as e:
            print(f"Error training face recognizer: {e}")
            speak("Error training face recognizer")
            return False
    
    @eel.expose
    def recognize_user(self):
        """
        Recognize user from webcam feed
        Returns: Recognized user name or None
        """
        try:
            if FACE_RECOGNIZER is None:
                speak("Face recognition needs opencv-contrib-python. Please install it and try again.")
                return None
            if not self.trained:
                if not self.train_face_recognizer():
                    return None
            
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                speak("Cannot access webcam")
                return None
            
            recognized_user = None
            confidence_threshold = 70
            frame_count = 0
            
            while frame_count < 30:
                ret, frame = cap.read()
                if not ret:
                    break
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)
                
                for (x, y, w, h) in faces:
                    face_roi = cv2.resize(gray[y:y+h, x:x+w], (200, 200))
                    label, confidence = FACE_RECOGNIZER.predict(face_roi)
                    
                    if confidence < confidence_threshold:
                        user_name = self.label_map.get(label, "Unknown")
                        recognized_user = user_name
                        speak(f"Welcome back, {user_name}!")
                        break
                
                frame_count += 1
            
            cap.release()
            cv2.destroyAllWindows()
            
            return recognized_user
            
        except Exception as e:
            print(f"Error during face recognition: {e}")
            return None

# Global face recognition manager
face_manager = FaceRecognitionManager()

@eel.expose
def activate_face_recognition():
    """Activate face recognition for greeting"""
    user = face_manager.recognize_user()
    if user:
        return user
    return None

@eel.expose
def register_new_user(user_name):
    """Register a new user via face recognition"""
    return face_manager.register_face(user_name)
