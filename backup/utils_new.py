import pyautogui as pag
import datetime
import time
import win32ui
from win32gui import GetWindowText, GetForegroundWindow
import os

address_dictionary = {}
address_dictionary["Devansh"] = "Devansh.Purohit@emc.com"
address_dictionary["Aiman"] = "Aiman.Fatima@emc.com"
address_dictionary["Naman"] = "naman.kedia@dell.com"
address_dictionary["Partha"] = "partha.datta@dell.com"

def type_email_id(name_temp):
    print(name_temp)
    name_found = False
    # Find the email id
    name_str = name_temp.split(" ")
    final_str=""
    for name in name_str:
        if name in address_dictionary:
            email_id = address_dictionary[name]
            name_found = True
            break
        final_str+=name
    # print(email_id)
    if(name_found == True):
        pag.typewrite(email_id)
        pag.press('enter')
    else:
        pag.typewrite(final_str)
        pag.press('enter')
        return

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
        time.sleep(25)
    else:
        print("outlook is running")
        # Make outlook window active
    current_window = GetWindowText(GetForegroundWindow())

    while not ("Inbox - Devansh.Purohit@emc.com - Outlook" in current_window):
        current_window = GetWindowText(GetForegroundWindow())

    if "Inbox - Devansh.Purohit@emc.com - Outlook" in current_window:
        print("outlook opened")
    else:
        print("outlook could not be opened")
        return
    
    # Compose a new email by ctrl + N
    print("Composing new email")
    pag.hotkey("ctrlleft", "n")

    # To open a New Window
    current_window = GetWindowText(GetForegroundWindow())
    while not ("Untitled - Message (HTML)" in current_window):
        current_window = GetWindowText(GetForegroundWindow())
    if "Untitled - Message (HTML)" in current_window:
        # Add To:
        print("Adding Recipient's now (Say next to go to section)")
        while(True):
            print("say the name or email id of main recipient") 
            audio = r.listen(source)      
            try:
                name = r.recognize_google(audio)
                if(name == "next"):
                    break
                else:
                    type_email_id(name)
            except:
                print("Didn't get that, say that again")
                continue
        # Add cc
        pag.typewrite('\t')
        print("add more email ids to cc (Say Next to skip) ")
        while(True):
            print("say the name or email id of cc") 
            audio = r.listen(source)      
            try:
                name = r.recognize_google(audio)
                if(name == "next"):
                    break
                else:
                    type_email_id(name)
            except:
                print("Didn't get that, say that again")
                continue
        
        # Add Subject
        pag.typewrite('\t')
        print("Say the subject") 
        while True:    
            try:
                audio = r.listen(source)  
                subject = r.recognize_google(audio)
                pag.typewrite(subject)
                break
            except:
                print("Didn't get that, say that again")
                continue

        # Add Body
        pag.typewrite('\t')
        print("Say the email body")  
        while True:    
            try:
                audio = r.listen(source)  
                body = r.recognize_google(audio)
                pag.typewrite(body)
                break
            except:
                print("Didn't get that, say that again")
                continue
        # Send the mail

        time.sleep(10)
        pag.hotkey('ctrl', 'enter')
        print("Do you want to send the email?")
        while True:
            try:
                audio = r.listen(source)  
                acknowledge = r.recognize_google(audio)
                if acknowledge == "yes":
                    pag.hotkey('enter')
                else:
                    pag.hotkey('\t')
                    pag.hotkey('enter')
                break
            except:
                print("Didn't get that, say that again")
                continue

        print("Mail sent")

def take_screenshot():
    name = datetime.datetime.now()
    name  = name.strftime("%b %d %Y %H %M %S")
    name = name + ".jpg"
    pag.screenshot(name)
    print("screen shot taken")

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


