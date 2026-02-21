import threading
import numpy
import sounddevice
import speech_recognition
import cv2
import mediapipe as mp
import numpy as np

from tkinter import *

import pyttsx3
from pyttsx3 import speak

def print_speech(sound_indata, frames, time, status):
    get_audio = speech_recognition.AudioData((sound_indata[:, 0]*MAX_INT).astype(numpy.int16).tobytes(), SAMPLE_RATE, SAMPLE_WIDTH)
    
    try:
        print(interpreter.recognize_google(get_audio))
    except speech_recognition.UnknownValueError:
        # print("No one is speaking.")
        pass

print("Entered speaking mode. Start talking:")

def text_to_speech():
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

def count_fingers(hand_landmarks):
    print("hand_landmarks", hand_landmarks)
    tips = [8, 12, 16, 20]
    fingers = 0

    # Thumb
    if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
        fingers += 1

    # Other fingers
    for tip in tips:
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingers += 1

    return fingers

def finger_to_letter_say(word):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    if voices:
        engine.setProperty('voice', voices[1].id)
    engine.say(word)
    engine.runAndWait()

def finger_to_letter(count):
    mapping = {
        0: "raja",
        1: "has",
        2: "an",
        3: "ai",
        4: "girlfriend",
        5: "HELLO"
    }
    return mapping.get(count, "?")

def distance(point1, point2):
    return np.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2 + (point1.z - point2.z) ** 2)

def translateASL(hand_landmarks, face_landmarks, pose_landmarks):
    if hand_landmarks and face_landmarks:
        if distance(hand_landmarks.landmark[4], face_landmarks.landmark[1]) < 0.2 and \
                distance(hand_landmarks.landmark[8], face_landmarks.landmark[1]) < 0.2 and \
                distance(hand_landmarks.landmark[12], face_landmarks.landmark[1]) < 0.2 and \
                distance(hand_landmarks.landmark[16], face_landmarks.landmark[1]) < 0.2 and \
                distance(hand_landmarks.landmark[20], face_landmarks.landmark[1]) < 0.2:
            return "food/eat"
        
        if distance(hand_landmarks.landmark[3], hand_landmarks.landmark[5]) >= 0.15 and \
                distance(hand_landmarks.landmark[8], hand_landmarks.landmark[5]) >= 0.2 and \
                distance(hand_landmarks.landmark[12], hand_landmarks.landmark[9]) <= 0.2 and \
                distance(hand_landmarks.landmark[16], hand_landmarks.landmark[13]) <= 0.2 and \
                distance(hand_landmarks.landmark[20], hand_landmarks.landmark[17]) >= 0.2:
            return "i love you"
         

    if hand_landmarks:
        if hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y and \
                hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y and \
                hand_landmarks.landmark[16].y > hand_landmarks.landmark[14].y and \
                hand_landmarks.landmark[20].y > hand_landmarks.landmark[18].y and \
                hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x:
            return "peace"

    return ""

MAX_INT = 32767

SAMPLE_RATE = 16000
SAMPLE_WIDTH = 2
BLOCK_SIZE = 80000

interpreter = speech_recognition.Recognizer()

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

t1 = threading.Thread(target=text_to_speech, daemon=True)
t1.start()

cap = cv2.VideoCapture(0)
with mp_holistic.Holistic(
        min_detection_confidence=0.5, 
        min_tracking_confidence=0.5
    ) as holistic, mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    ) as hands, sounddevice.InputStream(callback = print_speech, channels = 1, samplerate = SAMPLE_RATE, blocksize = BLOCK_SIZE):
    while cap.isOpened():

        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        image = cv2.flip(image, 1)

        results_hands = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = holistic.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            image,
            results.face_landmarks,
            mp_holistic.FACEMESH_CONTOURS,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing_styles
            .get_default_face_mesh_contours_style())
        mp_drawing.draw_landmarks(
            image,
            results.pose_landmarks,
            mp_holistic.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles
            .get_default_pose_landmarks_style())
        
        word = ""
        if results_hands.multi_hand_landmarks:
            for hand_landmarks in results_hands.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                word = translateASL(hand_landmarks, results.face_landmarks, results.pose_landmarks)

                # fingers = count_fingers(hand_landmarks)
                # word = finger_to_letter(fingers)
                
        finger_to_letter_say(word)
        cv2.putText(image, word, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('MediaPipe Holistic', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()