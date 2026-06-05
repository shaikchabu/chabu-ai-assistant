import os
import pyautogui
from PyPDF2 import PdfReader
from datetime import datetime
import cv2

def take_photo():
    """Captures a photo from the default camera and saves it."""
    try:
        shot_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "screenshots"))
        if not os.path.exists(shot_dir):
            os.makedirs(shot_dir)
            
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"photo_{timestamp}.jpg"
        filepath = os.path.join(shot_dir, filename)
        
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return "Failed to access the camera."
            
        ret, frame = cap.read()
        if ret:
            cv2.imwrite(filepath, frame)
            cap.release()
            os.startfile(shot_dir)
            return f"Photo captured and saved! Filename: {filename}"
        else:
            cap.release()
            return "Camera accessed but failed to read frame."
    except Exception as e:
        return f"Error taking photo: {str(e)}"

def take_screenshot():
    """Takes a screenshot and saves it to the 'screenshots' folder."""
    try:
        # Create screenshots directory if it doesn't exist
        shot_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "screenshots"))
        if not os.path.exists(shot_dir):
            os.makedirs(shot_dir)
            
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"screenshot_{timestamp}.png"
        filepath = os.path.join(shot_dir, filename)
        
        pyautogui.screenshot(filepath)
        # Open the folder so the user can see it
        os.startfile(shot_dir)
        return f"Screenshot saved and folder opened! Filename: {filename}"
    except Exception as e:
        return f"Failed to take screenshot: {str(e)}"

def read_pdf_text(file_name):
    """Extracts text from a PDF file in the current or documents directory."""
    try:
        # Check current directory and Documents
        possible_paths = [
            os.path.abspath(file_name),
            os.path.join(os.path.expanduser("~"), "Documents", file_name),
            os.path.abspath(os.path.join(os.path.dirname(__file__), "..", file_name))
        ]
        
        target_path = None
        for path in possible_paths:
            if not path.endswith(".pdf"):
                path += ".pdf"
            if os.path.exists(path):
                target_path = path
                break
                
        if not target_path:
            return f"I couldn't find the PDF file named '{file_name}'. Make sure it's in your Documents or project folder."
            
        reader = PdfReader(target_path)
        text = ""
        # Extract first 5 pages to avoid overloading
        for i in range(min(5, len(reader.pages))):
            text += reader.pages[i].extract_text()
            
        return text if text else "The PDF seems to be empty or contains no readable text."
        
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def list_files_in_dir(directory_name):
    """Lists files in common folders like Documents, Downloads, or Desktop."""
    try:
        dirs = {
            "documents": os.path.join(os.path.expanduser("~"), "Documents"),
            "document": os.path.join(os.path.expanduser("~"), "Documents"),
            "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
            "download": os.path.join(os.path.expanduser("~"), "Downloads"),
            "desktop": os.path.join(os.path.expanduser("~"), "Desktop")
        }
        
        target_dir = dirs.get(directory_name.lower())
        if not target_dir or not os.path.exists(target_dir):
            return f"I couldn't access the {directory_name} folder."
            
        files = os.listdir(target_dir)
        # Filter for common files and limit to 10
        files = [f for f in files if not f.startswith(".")][:10]
        
        if not files:
            return f"The {directory_name} folder is empty."
            
        return f"Here are the top files in your {directory_name}: " + ", ".join(files)
    except Exception as e:
        return f"Error listing files: {str(e)}"

def open_folder(folder_name):
    """Opens common folders in File Explorer."""
    try:
        dirs = {
            "documents": os.path.join(os.path.expanduser("~"), "Documents"),
            "document": os.path.join(os.path.expanduser("~"), "Documents"),
            "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
            "download": os.path.join(os.path.expanduser("~"), "Downloads"),
            "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
            "pictures": os.path.join(os.path.expanduser("~"), "Pictures"),
            "picture": os.path.join(os.path.expanduser("~"), "Pictures")
        }
        
        target_dir = dirs.get(folder_name.lower())
        if not target_dir:
            if not folder_name or "explorer" in folder_name.lower():
                target_dir = os.path.expanduser("~")
            else:
                return f"I don't know how to open the {folder_name} folder yet."
                
        if not os.path.exists(target_dir):
            return f"The {folder_name} folder does not exist."
            
        os.startfile(target_dir)
        name = folder_name if folder_name else "file explorer"
        return f"Opening {name}."
    except Exception as e:
        return f"Error opening folder: {str(e)}"

def find_and_open_file(file_query):
    """Searches Desktop, Documents, and Downloads for files matching query and opens them."""
    search_dirs = {
        "Desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
        "Documents": os.path.join(os.path.expanduser("~"), "Documents"),
        "Downloads": os.path.join(os.path.expanduser("~"), "Downloads")
    }
    
    supported_exts = {".pdf", ".docx", ".txt", ".pptx"}
    matches = []
    
    def normalize(s):
        return s.replace("_", "").replace("-", "").replace(" ", "").lower()
        
    query = file_query.strip().lower()
    if not query:
        return "Please specify a file name to open."
        
    has_ext = any(query.endswith(ext) for ext in supported_exts)
    norm_query = normalize(query)
    
    for dir_name, dir_path in search_dirs.items():
        if not os.path.exists(dir_path):
            continue
        try:
            for item in os.listdir(dir_path):
                item_path = os.path.join(dir_path, item)
                if not os.path.isfile(item_path):
                    continue
                    
                item_lower = item.lower()
                name_part, ext = os.path.splitext(item_lower)
                
                if ext not in supported_exts:
                    continue
                    
                if has_ext:
                    if normalize(item_lower) == norm_query:
                        matches.append((dir_name, item, item_path))
                else:
                    norm_name = normalize(name_part)
                    if norm_query == norm_name or norm_query in norm_name:
                        matches.append((dir_name, item, item_path))
        except Exception:
            pass
            
    if not matches:
        return f"I couldn't find any file matching '{file_query}' in Desktop, Documents, or Downloads."
        
    if len(matches) == 1:
        dir_name, file_name, file_path = matches[0]
        try:
            os.startfile(file_path)
            return f"Opening '{file_name}' from your {dir_name} folder."
        except Exception as e:
            return f"Found '{file_name}' in {dir_name}, but error opening it: {str(e)}"
            
    # Multiple matches found
    match_list = [f"'{m[1]}' in {m[0]}" for m in matches]
    return f"I found multiple files: {', '.join(match_list)}. Please specify the full name."

