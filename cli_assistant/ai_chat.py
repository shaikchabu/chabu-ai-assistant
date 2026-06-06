from google import genai
import os
import sys

# Ensure shared modules can be found
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared.memory import recall
from shared.logger import get_recent_history

from dotenv import load_dotenv

# Load .env file
env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
load_dotenv(env_path)

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY) if API_KEY else None
# ANSI Colors for a premium terminal feel
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def ask_ai(prompt):
    if not client:
        return "AI needs GEMINI_API_KEY in your .env file. Voice commands like open google still work."
    try:
        # 1. Fetch Context
        history = get_recent_history(limit=5) # Reduced limit for cleaner context
        personality = recall("personality") or "professional"
        user_name = recall("username") or "User"

        # 2. Build System Instructions based on personality
        personalities = {
            "funny": "You are a witty assistant. Use puns and jokes. Keep responses short and funny.",
            "professional": "You are a polished executive assistant. Be concise and formal.",
            "teacher": "You are a patient teacher. Explain things simply.",
            "friend": "You are a warm best friend. Be casual and caring."
        }
        
        system_instr = personalities.get(personality.lower(), personalities["professional"])
        
        # Inject context into the prompt
        full_prompt = f"System: {system_instr}\nYou are a highly advanced multilingual AI assistant named Chabu. If the user asks a question in Hindi, Telugu, or any other language, you MUST reply entirely in that exact same language. Do not reply in English if they spoke another language.\nUser Name: {user_name}\nRecent History:\n{history}\n\nCurrent Question: {prompt}"

        # 3. Call Gemini
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=full_prompt
        )

        clean_text = response.text.replace("*", "").strip()
        return clean_text

    except Exception as e:
        
        return f"AI Error: {str(e)}"

# ─────────────────────────────────────────────
# INTENT CLASSIFIER
# Maps natural language to exact canonical commands.
# Returns a canonical command string or "NO_INTENT".
# ─────────────────────────────────────────────
CANONICAL_COMMANDS = """
change to funny | change to professional | change to teacher | change to friend
my name is [name] | who am i
open youtube | open google | open chrome | open chatgpt | open linkedin | open whatsapp
take a screenshot | take a photo | check system
list my [folder] | open [folder] folder | open file [name]
analyze [filename]
remember [note text] | show notes | delete note [N]
add task [task text] | show tasks | complete task [N] | delete task [N]
remind me [msg] at [HH:MM] | write email [topic] | plan my day
forget everything | hello | search wikipedia [topic] | play [media name] | exit
"""

INTENT_PROMPT = f"""
You are an intent classifier for a voice AI assistant called Chabu.

Your job is to map a user's natural language input to ONE exact canonical command from the approved list below.

## APPROVED CANONICAL COMMANDS:
{CANONICAL_COMMANDS.strip()}

## RULES:
1. Return ONLY the exact canonical form. No explanation, no punctuation, no extra words.
2. Replace placeholders like [name], [N], [topic], [msg], [filename], [folder], [media name], [task text], [note text] with the actual value from the user's query.
3. For time in reminders — convert to 24-hour HH:MM format. "3 PM" → "15:00", "7:30 AM" → "07:30".
4. If the query is a general knowledge question, conversation, or does not match any command — return exactly: NO_INTENT
5. Do NOT invent new commands outside this list.

## EXAMPLES:
User: "can you launch youtube" → open youtube
User: "show me my notes" → show notes
User: "what tasks do i have" → show tasks
User: "remind me to drink water at 3 PM" → remind me drink water at 15:00
User: "what is the speed of light?" → NO_INTENT
User: "tell me a joke" → NO_INTENT
User: "remove note 2" → delete note 2
User: "make yourself funny" → change to funny
User: "open my resume" → open file resume
User: "mark task 3 as done" → complete task 3

User input: {{user_input}}
Canonical command:"""


def classify_intent(user_input: str) -> str:
    """Classify user input into a canonical command using Gemini, or return NO_INTENT."""
    if not client:
        return "NO_INTENT"
    try:
        prompt = INTENT_PROMPT.replace("{user_input}", user_input.strip())
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )
        result = response.text.strip().lower().rstrip(".")
        # Safety: reject empty or suspiciously long results (not a valid canonical command)
        if not result or len(result) > 120:
            return "NO_INTENT"
        return result
    except Exception:
        return "NO_INTENT"

