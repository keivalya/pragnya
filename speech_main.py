import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('rate', 145)

def speak(voice_control="CS", sentence=None):
    if voice_control == "CS":
        engine.setProperty('voice', voices[1].id)
    elif voice_control == "ST":
        engine.setProperty('voice', voices[0].id)
        pass
    engine.say(sentence)
    print(sentence)
    engine.runAndWait()

# sentence = "The housing is brought to the delivery platform."
# speak(sentence=sentence) 