from tkinter import *

import pyttsx3
from pyttsx3 import speak

window = Tk()
window.title("Speech Box")

text_box = Entry(window, width = 70)
text_box.pack()

text_box.focus_set()

engine = pyttsx3.init()
voices = engine.getProperty('voices')

if voices:
    engine.setProperty('voice', voices[1].id)

def text_to_speech():
    engine.say(text_box.get())
    engine.runAndWait()

speak_button = Button(window, text = "Speak", width = 20, height = 2, command = text_to_speech)
speak_button.pack()

mainloop()