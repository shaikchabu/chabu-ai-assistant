import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from speech_engine import listen, speak
from command_processor import process_command
from shared.logger import set_status
from shared.reminders import start_reminder_thread
from wake_word import WAKE_PHRASE, is_wake_command


def main():
    start_reminder_thread()
    os.system("cls" if os.name == "nt" else "clear")

    print("==========================================")
    print("       CHABU AI - Your Voice Your Control")
    print("==========================================\n")
    print("VOICE WINDOW — keep this open for microphone + speaker\n")

    print("Assistant: Chabu AI Assistant is live now.")
    speak("Chabu AI Assistant is live now.")

    is_awake = False
    set_status("Standing By", is_awake=False)
    print(f"\nAssistant: Standing by... (Say '{WAKE_PHRASE}' to wake me up)\n")

    while True:
        set_status("Listening...", is_awake=is_awake)
        command = listen()

        if not command or not command.strip():
            continue

        cmd_lower = command.lower()

        if not is_awake:
            if is_wake_command(cmd_lower):
                is_awake = True
                set_status("Awake", is_awake=True)
                print("\n[WAKE WORD DETECTED]")
                speak("I am here. How can I help you?")
                continue
            if any(w in cmd_lower for w in ("exit", "shutdown", "terminate", "quit")):
                set_status("Shutting Down", is_awake=False)
                speak("Goodbye.")
                break
            continue

        set_status("Processing...", is_awake=True)
        response = process_command(command)

        if response == "exit":
            print("Assistant: Goodbye!")
            speak("Goodbye")
            break

        if response:
            try:
                print(f"Assistant: {response}")
            except UnicodeEncodeError:
                safe_response = response.encode(sys.stdout.encoding or 'cp1252', errors='replace').decode(sys.stdout.encoding or 'cp1252')
                print(f"Assistant: {safe_response}")
            set_status("Speaking...", is_awake=True)
            speak(response)


if __name__ == "__main__":
    main()
