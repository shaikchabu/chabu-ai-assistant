import pyttsx3
engine = pyttsx3.init()
engine.say("Testing speech engine")
engine.runAndWait()
print("Speech should have finished")
