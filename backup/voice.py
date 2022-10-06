import speech_recognition as sr

import pyautogui as pag
import datetime
import os
import time
from utils_new import *


r = sr.Recognizer()
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    while True:   
        print("Say Something") 
        audio = r.listen(source)      
        try:
            text = r.recognize_google(audio)
            tokenized_text = text.split(" ")
            print("TEXT: "+text)
            if text == "send an email":
                send_email(source, r)
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