import os
import time
import pyautogui

# Open WhatsApp Desktop
os.system("start whatsapp:")
time.sleep(5)

# Click search bar
pyautogui.click(200, 150)

# Search contact
pyautogui.write("gouse", interval=0.05)
time.sleep(2)

# Open first result
pyautogui.press("enter")
time.sleep(1)

# Type message
pyautogui.write("Hello from Chabu AI!", interval=0.05)

# Send
pyautogui.press("enter")