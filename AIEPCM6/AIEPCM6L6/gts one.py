import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import pygame
import os

translator = Translator()
pygame.mixer.init()
# Speak translated text
def speak(text, lang):
    tts = gTTS(text=text, lang=lang)
    filename = "voice.mp3"
    tts.save(filename)
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    pygame.mixer.music.unload()

    os.remove(filename)
# Convert speech to text
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Speak now...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        print(f"✅ You said: {text}")
        return text
    except:
        print("❌ Could not recognize speech")
        return ""
# Main Program

def main():
    languages = {
        "1": ("Hindi", "hi"),
        "2": ("French", "fr"),
        "3": ("Spanish", "es")
    }
    print("🌍 Select Language:")
    print("1. Hindi")
    print("2. French")
    print("3. Spanish")
    choice = input("Enter choice: ")
    language_name, language_code = languages.get(choice, ("Hindi", "hi"))
    print(f"✅ Selected: {language_name}")
    while True:
        text = speech_to_text()
        if text.lower() == "exit":
            speak("Goodbye", "en")
            break
        translated = translator.translate(
            text,
            dest=language_code
        )
        print(f"🌍 Translation: {translated.text}")
        speak(translated.text, language_code)
if __name__ == "__main__":

    main()
