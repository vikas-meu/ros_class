import cv2
import mediapipe as mp
import math
import serial
import time
import numpy as np
 
ser = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)
 
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

 
MIN_DIST = 30      
MAX_DIST = 200     

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            lm = hand_landmarks.landmark

            
            x1, y1 = int(lm[4].x * w), int(lm[4].y * h)
            x2, y2 = int(lm[8].x * w), int(lm[8].y * h)

            
            cv2.circle(frame, (x1, y1), 8, (255, 0, 0), -1)
            cv2.circle(frame, (x2, y2), 8, (255, 0, 0), -1)
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

             
            dist = math.hypot(x2 - x1, y2 - y1)

             
            angle = np.interp(dist, [MIN_DIST, MAX_DIST], [0, 180])
            angle = int(np.clip(angle, 0, 180))

             
            ser.write(f"{angle}\n".encode())

            
            cv2.putText(frame, f"Dist: {int(dist)}", (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, f"Servo: {angle}", (20, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            mp_draw.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
            )

    cv2.imshow("Finger Distance Servo Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
ser.close()
cv2.destroyAllWindows()
