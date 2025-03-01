import pyttsx3

def text_to_speech(text, rate=190):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()

# Test the function with a sample text
text_to_speech("Guys, how does this sound? Is it too fast or slow?")
