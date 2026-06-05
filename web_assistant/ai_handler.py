import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cli_assistant.command_processor import process_command
from shared.logger import set_status

def process_web_command(command):
    """Bridge for the Streamlit UI to call the main processing logic."""
    set_status("Processing...", is_awake=True)
    response = process_command(command)
    set_status("Ready", is_awake=True)
    return response
