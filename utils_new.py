import pyautogui as pag
import datetime
import time
import win32ui
import win32gui
import os
import json

def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

results = []
top_windows = []
f = open("person.json", "r")
address_dictionary = json.load(f)
# address_dictionary["Path"] = "partha.datta@dell.com"

# def add_to_dict(name, address):
#     if name not in address_dictionary:




# IMPORTANT: type out the recipient email id through spelling or dict
def type_email_id(name_temp):
  
    if len(name_temp)==2:
        print("log: in len temp 2.")
        if name_temp[1] in address_dictionary:
            print("log: found name in dictionary")
            email_id = address_dictionary[name_temp[1]]
            pag.typewrite(email_id)
            pag.press('enter')
        else:
            pag.typewrite(name_temp[1])
            print("log:did not find name in dict")
            pag.press('enter')


    else:
        temp = ""
        for i in range(1, len(name_temp)):
            if name_temp[i] == 'at':
                temp = temp + '@'
            elif name_temp[i] == 'dot':
                temp = temp + '.'
            else:
                temp = temp + name_temp[i]
        email_id = temp
        pag.typewrite(email_id)
        pag.press('enter')
   

def outlook_is_running():
    try:
        win32ui.FindWindow(None, "Microsoft Outlook")
        return True
    except win32ui.error:
        return False


def send_email(source, r):
    if not outlook_is_running():
        print("Opening outlook! Please wait")
        os.startfile("outlook")
        time.sleep(35)
    else:
        print("outlook is running")
        win32gui.EnumWindows(windowEnumerationHandler, top_windows)
        print("Trying to bring ol to the front! 1")
        for i in top_windows:
            if "- Outlook" in i[1]:
                win32gui.ShowWindow(i[0],5)
                win32gui.SetForegroundWindow(i[0])
        # Make outlook window active

#IGNORE
    current_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    # while not ("Inbox - Devansh.Purohit@emc.com - Outlook" in current_window):
    #     current_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())

    if "Inbox - Devansh.Purohit@emc.com - Outlook" in current_window:
        print("outlook opened")
    else:
        print("outlook could not be opened")
        # return
    
    # Compose a new email by ctrl + N
    print("Composing new email")
    pag.hotkey("ctrlleft", "n")

   
def take_screenshot():
    name = datetime.datetime.now()
    name  = name.strftime("%b %d %Y %H %M %S")
    name = name + ".jpg"
    pag.screenshot(name)
    print("screenshot taken")

def type_something(text):
    tokenized_text = text.split(" ")
    for i in range(1, len(tokenized_text)):
        pag.typewrite(tokenized_text[i]+" ")

def select_all():
    pag.hotkey("ctrlleft", "a")
    print("all selected")

def copy():
    pag.hotkey("ctrlleft", "c")
    print("copied!!")

def paste():
    pag.hotkey("ctrlleft", "v")
    print("pasted")

def press_enter():
    pag.press('enter')


