import speech_recognition as sr
import pyautogui as pag
import datetime
import os
import time
import json
# from utils import *
from utils_new import *
from win10toast import ToastNotifier

toaster = ToastNotifier()
r = sr.Recognizer()


while True:
    with sr.Microphone() as source:
        r.pause_threshold = 1
        
        r.adjust_for_ambient_noise(source)
        print("Say Something")
        toaster.show_toast("Say something")
        try: 
            audio = r.listen(source, 5)  
        except:
            continue
            
        print("Audio has finished recording")  
        # toaster.show_toast("Audio has finished recording")  
        try:
            text = r.recognize_google(audio)
            print("Text has been recognized")
            # toaster.show_toast("Text has been recognized")
            tokenized_text = text.split(" ")
            print("TEXT: "+text)
            toaster.show_toast(text)

            if text == "send an email":
                send_email(source, r)

            elif tokenized_text[0] == "include":
                print("printing name as email address")
                type_email_id(tokenized_text)

            elif text == "take screenshot":
                take_screenshot()

            elif tokenized_text[0] == "type":
                type_something(text)

            elif text == "select all":
                select_all()

            elif text == "copy":
                copy()

            elif text == "paste":
                paste()

            elif text == "press enter":
                press_enter()

            elif text == "exit":
                break

            else:
                print("Wrong Command, try again")
            
        except:
            print("Sorry, I didn't get you!")
            continue

# convSpeechToText()