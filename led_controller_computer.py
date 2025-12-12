import cv2
import mediapipe as mp
import serial
import time
 
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

led_state = None   

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    gesture = "No Hand"

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            lm = hand_landmarks.landmark

            
            thumb_tip_y = lm[4].y
            wrist_y = lm[0].y

            
            if thumb_tip_y < wrist_y - 0.05:
                gesture = "Thumbs UP  → LED ON"
                if led_state != 1:
                    ser.write(b'1')
                    led_state = 1

            elif thumb_tip_y > wrist_y + 0.05:
                gesture = "Thumbs DOWN → LED OFF"
                if led_state != 0:
                    ser.write(b'0')
                    led_state = 0

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )
 
    cv2.rectangle(frame, (20, 20), (420, 80), (0, 0, 0), -1)
    cv2.putText(
        frame,
        gesture,
        (30, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Thumb Gesture LED Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
ser.close()
cv2.destroyAllWindows()
