import cv2
import mediapipe as mp
import math
from collections import Counter, deque


# ==========================================
# WEBCAM
# ==========================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Could not open webcam")
    exit()

print("✅ Webcam opened successfully")


# ==========================================
# MEDIAPIPE
# ==========================================

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6
)


# ==========================================
# GESTURE HISTORY
# ==========================================

gesture_history = deque(maxlen=7)


# ==========================================
# DISTANCE FUNCTION
# ==========================================

def distance(p1, p2):

    return math.sqrt(
        (p1.x - p2.x) ** 2 +
        (p1.y - p2.y) ** 2
    )


# ==========================================
# FINGER DETECTION
# ==========================================

def get_finger_states(landmarks, handedness):

    # --------------------------------------
    # Index finger
    # --------------------------------------

    index_open = (
        landmarks[8].y <
        landmarks[6].y
    )


    # --------------------------------------
    # Middle finger
    # --------------------------------------

    middle_open = (
        landmarks[12].y <
        landmarks[10].y
    )


    # --------------------------------------
    # Ring finger
    # --------------------------------------

    ring_open = (
        landmarks[16].y <
        landmarks[14].y
    )


    # --------------------------------------
    # Pinky finger
    # --------------------------------------

    pinky_open = (
        landmarks[20].y <
        landmarks[18].y
    )


    # --------------------------------------
    # Thumb
    # --------------------------------------

    thumb_tip = landmarks[4]
    thumb_mcp = landmarks[2]

    thumb_tip_distance = distance(
        thumb_tip,
        landmarks[5]
    )

    thumb_mcp_distance = distance(
        thumb_mcp,
        landmarks[5]
    )

    thumb_open = (
        thumb_tip_distance >
        thumb_mcp_distance * 1.3
    )


    return (
        thumb_open,
        index_open,
        middle_open,
        ring_open,
        pinky_open
    )


# ==========================================
# GESTURE DETECTION
# ==========================================

def detect_gesture(landmarks, handedness):

    (
        thumb,
        index,
        middle,
        ring,
        pinky
    ) = get_finger_states(
        landmarks,
        handedness
    )


    # ======================================
    # FIST ✊
    # ======================================

    if (
        not thumb
        and not index
        and not middle
        and not ring
        and not pinky
    ):

        return "FIST"


    # ======================================
    # THUMBS UP 👍
    # ======================================

    if (
        thumb
        and not index
        and not middle
        and not ring
        and not pinky
    ):

        # Thumb must point upward

        if landmarks[4].y < landmarks[3].y:
            return "THUMBS UP"


    # ======================================
    # VICTORY ✌️
    # ======================================

    if (
        index
        and middle
        and not ring
        and not pinky
    ):

        return "VICTORY"


    # ======================================
    # INDEX ☝️
    # ======================================

    if (
        index
        and not middle
        and not ring
        and not pinky
    ):

        return "INDEX"


    # ======================================
    # OPEN HAND ✋
    # ======================================

    if (
        thumb
        and index
        and middle
        and ring
        and pinky
    ):

        return "OPEN HAND"


    return "UNKNOWN"


# ==========================================
# START MESSAGE
# ==========================================

print()
print("======================================")
print("      AI HAND GESTURE DETECTION")
print("======================================")
print()
print("Gestures:")
print("☝️  INDEX")
print("👍  THUMBS UP")
print("✌️  VICTORY")
print("✋  OPEN HAND")
print("✊  FIST")
print()
print("Press Q to quit.")
print("======================================")
print()


# ==========================================
# MAIN CAMERA LOOP
# ==========================================

print("🎥 Camera loop started...")


while True:

    # --------------------------------------
    # Read frame
    # --------------------------------------

    success, frame = cap.read()

    if not success:

        print("❌ Could not read camera frame")
        break


    # --------------------------------------
    # Flip camera
    # --------------------------------------

    frame = cv2.flip(
        frame,
        1
    )


    # --------------------------------------
    # Convert BGR → RGB
    # --------------------------------------

    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    # --------------------------------------
    # MediaPipe processing
    # --------------------------------------

    results = hands.process(
        rgb_frame
    )


    current_gesture = "NO HAND"
    handedness = ""


    # ======================================
    # HAND DETECTED
    # ======================================

    if results.multi_hand_landmarks:

        for hand_landmarks, handedness_info in zip(
            results.multi_hand_landmarks,
            results.multi_handedness
        ):

            # Draw hand landmarks

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )


            # Get hand side

            handedness = (
                handedness_info
                .classification[0]
                .label
            )


            # Detect gesture

            current_gesture = detect_gesture(
                hand_landmarks.landmark,
                handedness
            )


    # ======================================
    # GESTURE STABILIZATION
    # ======================================

    if current_gesture != "UNKNOWN":

        gesture_history.append(
            current_gesture
        )


    if len(gesture_history) >= 4:

        stable_gesture = Counter(
            gesture_history
        ).most_common(1)[0][0]

    else:

        stable_gesture = current_gesture


    # ======================================
    # DISPLAY GESTURE
    # ======================================

    cv2.putText(
        frame,
        "Gesture: " + stable_gesture,
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )


    # ======================================
    # DISPLAY HAND SIDE
    # ======================================

    if handedness:

        cv2.putText(
            frame,
            "Hand: " + handedness,
            (20, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2
        )


    # ======================================
    # DISPLAY WINDOW
    # ======================================

    cv2.imshow(
        "AI Hand Gesture Detection",
        frame
    )


    # ======================================
    # PRESS Q TO QUIT
    # ======================================

    if cv2.waitKey(1) & 0xFF == ord("q"):

        break


# ==========================================
# CLEANUP
# ==========================================

cap.release()

hands.close()

cv2.destroyAllWindows()

print()
print("✅ Program closed.")
