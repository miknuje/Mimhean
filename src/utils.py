import pyttsx3
import speech_recognition as sr

def falar(texto):
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()

def ouvir():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            print("Ouvindo...")
            audio = recognizer.listen(source)
            comando = recognizer.recognize_google(audio, language="pt-PT")
            return comando
        except sr.UnknownValueError:
            return None
