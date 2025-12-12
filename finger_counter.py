import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

 
TIP_IDS = [4, 8, 12, 16, 20]
 
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    result = hands.process(rgb)

    finger_count = 0

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
          
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            lm = hand_landmarks.landmark

            
            if lm[TIP_IDS[0]].x > lm[TIP_IDS[0] - 1].x:
                finger_count += 1

            
            for i in range(1, 5):
                if lm[TIP_IDS[i]].y < lm[TIP_IDS[i] - 2].y:
                    finger_count += 1

 
    cv2.rectangle(frame, (20, 20), (160, 80), (0, 0, 0), -1)
    cv2.putText(
        frame,
        f"Fingers: {finger_count}",
        (30, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.2,
        (0, 255, 0),
        3
    )

    cv2.imshow("Finger Skeleton & Count", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
