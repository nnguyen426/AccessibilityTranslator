import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

def count_fingers(hand_landmarks):
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

def finger_to_letter(count):
    mapping = {
        0: "A",
        1: "D",
        2: "V",
        3: "W",
        4: "B",
        5: "HELLO"
    }
    return mapping.get(count, "?")

cap = cv2.VideoCapture(0)
with mp_holistic.Holistic(
        min_detection_confidence=0.5, 
        min_tracking_confidence=0.5
    ) as holistic, mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    ) as hands:
    while cap.isOpened():

        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        image = cv2.flip(image, 1)

        results_hands = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        letter = ""
        if results_hands.multi_hand_landmarks:
            for hand_landmarks in results_hands.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                fingers = count_fingers(hand_landmarks)
                letter = finger_to_letter(fingers)

        cv2.putText(image, letter, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

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

        cv2.imshow('MediaPipe Holistic', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
cap.release()