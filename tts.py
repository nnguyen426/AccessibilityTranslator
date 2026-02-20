import pyttsx3

engine = pyttsx3.init()
exit = False
while exit == False:
    say=input("type what to say: ")

    voices = engine.getProperty('voices')
    if len(voices) > 0 and say != "00001":
        engine.say(say)
        engine.runAndWait()
    else:
        print("exiting")
    if say == "00001":
        exit = True
    