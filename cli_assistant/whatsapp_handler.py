import os
import time
import json
import pyautogui
pyautogui.FAILSAFE = False


def send_whatsapp(contact, message):

    os.system("start whatsapp:")
    time.sleep(5)

    # Use YOUR working search-bar coordinates
    pyautogui.click(200, 150)

    pyautogui.write(contact, interval=0.05)

    time.sleep(2)

    pyautogui.press("enter")

    time.sleep(3)

    pyautogui.write(message, interval=0.05)
    time.sleep(1)

    pyautogui.press("enter")

    return f"Message sent to {contact}"




def send_to_all(message):
    with open("contacts_local.json", "r") as f:
        contacts = json.load(f)

    for contact_name in contacts.keys():
        send_whatsapp(contact_name, message)
        time.sleep(5)  

    return f"Message sent to {len(contacts)} contacts."