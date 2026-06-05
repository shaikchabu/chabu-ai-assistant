import webbrowser
import wikipedia
import random
import os
import platform
import sys

# Ensure shared modules can be found
from cli_assistant.whatsapp_handler import send_to_all, send_whatsapp
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cli_assistant.ai_chat import ask_ai, classify_intent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from shared.memory import remember, recall, save_memory
from shared.logger import save_chat
from shared.system_tools import take_screenshot, read_pdf_text, list_files_in_dir, take_photo, open_folder, find_and_open_file
from shared.notes_tasks import add_note, get_notes, add_task, get_tasks, complete_task, delete_note, delete_task
from shared.reminders import add_reminder
from shared.app_launcher import open_application


def open_website(url):
    """Open URL in browser — works from voice CLI and web dashboard."""
    try:
        if not webbrowser.open(url, new=2):
            if os.name == "nt":
                os.startfile(url)
    except Exception:
        if os.name == "nt":
            os.system(f'start "" "{url}"')


def normalize_username(raw_name):
    """Clean up speech-to-text mistakes for stored username."""
    name = " ".join(raw_name.split())
    # e.g. "c h a b u" or "sabu c h a b u" from misheard "chabu"
    if "chabu" in name.replace(" ", ""):
        return "Chabu"
    letters = name.split()
    if len(letters) > 1 and all(len(tok) == 1 for tok in letters):
        return "".join(letters).title()
    return name.title()


def process_command(command, _classified=False):
    command = command.lower().strip()
    response = ""

    # --- PERSONALITY & USER INFO (Smarter matching to save Quota) ---
    if "personality" in command or "change to" in command:
        valid_p = ["funny", "professional", "teacher", "friend"]
        found = False
        for p in valid_p:
            if p in command:
                remember("personality", p)
                response = f"Personality updated! I am now your {p}."
                found = True
                break
        if not found and ("personality" in command):
            response = "You can change my personality to funny, professional, teacher, or friend."

    elif "my name is" in command or "call me" in command:
        name = command.replace("my name is", "").replace("call me", "").strip()
        name = normalize_username(name)
        remember("username", name)
        response = f"Got it! I'll call you {name} from now on."

    elif "who am i" in command or "my name" in command:
        name = recall("username")
        response = f"You are {name}, the creator of this AI!" if name else "I don't know your name yet. You can say 'my name is...' to tell me!"

    # --- WEB & FOLDER COMMANDS ---
    elif "open youtube" in command:
        open_website("https://www.youtube.com")
        response = "Opening YouTube for you!"

    elif "open google" in command:
        open_website("https://www.google.com")
        response = "Opening Google."

    elif "open chrome" in command:
        os.system("start chrome")
        response = "Launching Google Chrome."

    elif "open chatgpt" in command:
        open_website("https://chat.openai.com")
        response = "Opening ChatGPT."

    elif "open linkedin" in command:
        open_website("https://www.linkedin.com")
        response = "Opening LinkedIn."

    elif "open whatsapp" in command:
        os.system("start whatsapp://")
        response = "Opening WhatsApp Desktop."

    # --- SYSTEM INTELLIGENCE (Stage 6) ---
    elif "take a screenshot" in command or "capture my screen" in command:
        response = take_screenshot()

    elif "take a picture" in command or "open camera" in command or "take a photo" in command:
        response = take_photo()

    elif "analyze" in command or "read" in command or "analyse" in command:
        file_name = command.replace("analyze", "").replace("read", "").replace("analyse", "").replace("pdf", "").strip()
        if not file_name:
            response = "What file would you like me to analyze?"
        else:
            pdf_content = read_pdf_text(file_name)
            if "Error" in pdf_content or "couldn't find" in pdf_content:
                response = ask_ai(command)
            else:
                response = ask_ai(f"Extracted text from '{file_name}': {pdf_content[:3000]}. Please summarize/answer questions.")

    elif any(phrase in command for phrase in ["what is in my", "what's in my", "list my"]):
        folder = command.replace("what is in my", "").replace("what's in my", "").replace("list my", "").strip()
        response = list_files_in_dir(folder)

    elif "open" in command and any(f in command for f in ["folder", "file explorer", "desktop", "downloads", "documents", "pictures"]):
        folder = command.replace("open my", "").replace("open", "").replace("folder", "").replace("in file explorer", "").replace("file explorer", "").strip()
        response = open_folder(folder)

    elif command.startswith("open "):

       app_name = command.replace("open", "").strip()

       result = open_application(app_name)

       if result:
         response = result
       else:
        response = find_and_open_file(app_name)

    # --- NOTES & TASKS ---
    elif "remember:" in command or "remember " in command:
        note_text = command.replace("remember:", "").replace("remember ", "").strip()
        response = add_note(note_text)
        
    elif "show notes" in command or "read notes" in command:
        notes = get_notes()
        if not notes:
            response = "You don't have any notes."
        else:
            response = "Here are your notes:\n" + "\n".join([f"{i+1}. {n}" for i, n in enumerate(notes)])
            
    elif "delete note" in command:
        parts = command.split()
        if len(parts) >= 3 and parts[-1].isdigit():
            idx = int(parts[-1]) - 1
            response = delete_note(idx)
        else:
            response = "Please specify the note number to delete, like 'delete note 1'."
            
    elif "add task" in command or "add task:" in command:
        task_text = command.replace("add task:", "").replace("add task ", "").strip()
        response = add_task(task_text)
        
    elif "show tasks" in command or "read tasks" in command:
        tasks = get_tasks()
        if not tasks:
            response = "Your task list is empty."
        else:
            response = "Here are your tasks:\n"
            for i, t in enumerate(tasks):
                status = "Done" if t['completed'] else "Pending"
                response += f"{i+1}. {t['task']} [{status}]\n"
                
    elif "complete task" in command:
        parts = command.split()
        if len(parts) >= 3 and parts[-1].isdigit():
            idx = int(parts[-1]) - 1
            response = complete_task(idx)
        else:
            response = "Please specify the task number, like 'complete task 1'."
            
    elif "delete task" in command:
        parts = command.split()
        if len(parts) >= 3 and parts[-1].isdigit():
            idx = int(parts[-1]) - 1
            response = delete_task(idx)
        else:
            response = "Please specify the task number, like 'delete task 1'."

    # --- PRODUCTIVITY (Stage 4, 5, 6) ---
    elif "remind me:" in command or "remind me " in command:
        parts = command.replace("remind me:", "").replace("remind me ", "").strip().split(" at ")
        if len(parts) == 2:
            msg = parts[0]
            time_str = parts[1].replace(".", ":").strip()
            response = add_reminder(time_str, msg)
        else:
            response = "Please use the format: remind me [message] at [HH:MM]."

    elif "write email" in command or "write a mail" in command or "write mail" in command:
        prompt = command.replace("write email", "").replace("write a mail", "").replace("write mail", "").strip()
        if not prompt:
            response = "What would you like the email to be about? For example, say: 'write email asking for a day off'."
        else:
            response = ask_ai(f"Draft the exact body of a professional email for this request: '{prompt}'. Provide ONLY the drafted email. Do not give instructions on how to write it.")

    elif "plan my day" in command or "create schedule" in command:
        response = ask_ai("Create a productive and balanced daily schedule. Include study, work, and breaks.")

    # --- RESET ---
    elif "forget everything" in command or "clear history" in command:
        save_memory({})
        log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs", "chat_history.txt"))
        if os.path.exists(log_path):
            os.remove(log_path)
        return "Memory and history cleared."
    elif command.startswith("send message to "):

        try:
           parts = command.replace("send message to ", "").split(" saying ")

           contact = parts[0].strip()
           message = parts[1].strip()

           response = send_whatsapp(contact, message)

        except:
          response = "Use format: send message to mom saying hello"
    elif command.startswith("send to all "):

      msg = command.replace("send to all ", "").strip()

      response = send_to_all(msg)      


    # --- OTHER COMMANDS ---
    elif any(word in command for word in ["hello", "hi", "hii", "hey"]):
        name = recall("username")
        response = f"Hello {name if name else ''}! How can I help you today?"

    elif "check system" in command or "system info" in command:
        info = f"OS: {platform.system()} {platform.release()}\nProcessor: {platform.processor()}"
        response = info

    elif "search wikipedia" in command:
        topic = command.replace("search wikipedia", "").strip()
        try:
            response = wikipedia.summary(topic, sentences=2)
        except:
            response = "Wikipedia search failed."

    elif "play" in command:
        song = command.replace("play", "").strip()
        try:
            import pywhatkit
            pywhatkit.playonyt(song)
            response = f"Playing {song} on YouTube."
        except Exception as e:
            response = "Could not connect to YouTube right now."
   
    elif "exit" in command or "goodbye" in command:
      return "exit"

    elif "exit" in command or "goodbye" in command:
        return "exit"

    else:
        # ── INTENT CLASSIFICATION FALLBACK ──────────────────────────────
        # If the raw command didn't hit any hardcoded route, ask Gemini
        # to classify it into a canonical command from the approved catalog.
        # _classified=True prevents infinite recursion.
        if not _classified:
            intent = classify_intent(command)
            if intent and intent != "no_intent" and intent != command:
                # Re-route through the full processor with the canonical form
                response = process_command(intent, _classified=True)
                if response and response != "exit":
                    save_chat(command, response)
                return response
        # No intent matched — answer as a general AI conversation
        response = ask_ai(command)

    # --- SAVE TO HISTORY ---
    if response and response != "exit":
        save_chat(command, response)

    return response