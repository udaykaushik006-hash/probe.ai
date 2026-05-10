import speech_recognition as sr

def listen_wake_word():
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            audio = recognizer.listen(source, timeout=3)

        text = recognizer.recognize_google(audio).lower()

        return "hey probe" in text

    except:
        return False