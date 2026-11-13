import cv2
import mediapipe as mp

# Start webcam
cap = cv2.VideoCapture(0)

# MediaPipe Hand Detection
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

print("AI Hand Detection Started!")
print("Show your hand to the camera.")
print("Press Q to quit.")

while True:
    success, frame = cap.read()

    if not success:
        print("Could not read camera frame.")
        break

    # Flip camera so it feels natural
    frame = cv2.flip(frame, 1)

    # Convert BGR → RGB for MediaPipe
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect hands
    results = hands.process(rgb_frame)

    # Draw hand landmarks
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    cv2.imshow("AI Hand Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
hands.close()
cv2.destroyAllWindows()