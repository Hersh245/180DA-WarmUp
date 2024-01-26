import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Use the microphone as source for input
with sr.Microphone() as source:
    print("Speak Anything :")
    audio = recognizer.listen(source)

    try:
        # Recognize speech using Google Web Speech API
        text = recognizer.recognize_google(audio)
        print("You said : {}".format(text))
    except:
        print("Sorry could not recognize your voice")
