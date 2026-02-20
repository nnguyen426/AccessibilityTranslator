import cv2
import mediapipe as mp
import numpy as np

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

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

def run_asl_recognizer():
    cap = cv2.VideoCapture(0)

    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    ) as hands:

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)

            letter = ""

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                    )

                    finger_count = count_fingers(hand_landmarks)
                    letter = finger_to_letter(finger_count)

            cv2.putText(frame, f"Detected: {letter}", (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

            cv2.imshow("ASL Recognizer", frame)

            if cv2.waitKey(1) & 0xFF == 27:  # ESC key
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_asl_recognizer()