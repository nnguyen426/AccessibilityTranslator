import pyttsx3

engine = pyttsx3.init()
exit = False
voices =engine.getProperty('voices')
if voices:
    engine.setProperty('voice', voices[1].id)

while exit == False:
    say=input("type what to say!: ")
    

    if say == "00001":
        exit = True
        print("exiting")
    else:
        engine.runAndWait()
        engine.say(say)
    
    