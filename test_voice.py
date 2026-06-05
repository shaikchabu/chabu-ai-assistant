from cli_assistant.speech_engine import listen, speak

speak("Hello, I am Chabu AI.")

text = listen()

print("User said:", text)

speak(f"You said {text}")