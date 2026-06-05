import speech_recognition as sr
import win32com.client
import time
import msvcrt

recognizer = sr.Recognizer()
speaker = win32com.client.Dispatch("SAPI.SpVoice")


def speak(text):
    """Text to speech — Windows SAPI5. Press p=pause, s=stop while speaking."""
    text = str(text)
    if not text.strip():
        return
    try:
        speaker.Speak(text, 1)  # async
        is_paused = False
        while True:
            if speaker.Status.RunningState == 1:
                break
            if msvcrt.kbhit():
                key = msvcrt.getch().lower()
                if key == b"p":
                    if not is_paused:
                        speaker.Pause()
                        is_paused = True
                        print("\n[Paused - Press 'p' to Resume]")
                    else:
                        speaker.Resume()
                        is_paused = False
                        print("[Resumed]")
                elif key == b"s":
                    speaker.Speak("", 3)
                    print("\n[Speech Stopped]")
                    break
            time.sleep(0.05)
    except Exception as e:
        print(f"Voice Error: {e}")


def listen():
    """Listen to microphone — no short timeout (waits until you speak)."""
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            try:
                audio = recognizer.listen(source)
                print("Recognizing...")
                command = recognizer.recognize_google(audio, language="en-IN")
                print(f"You said: {command}")
                return command.lower()
            except sr.UnknownValueError:
                speak("Sorry, I did not understand.")
                return ""
            except sr.RequestError:
                speak("Speech service is unavailable.")
                return ""
            except Exception as e:
                print("Error:", e)
                speak("An error occurred.")
                return ""
    except (OSError, AttributeError):
        print("Microphone or Audio dependencies (PyAudio) not detected. Use the web dashboard for text commands.")
        time.sleep(10)
        return ""
