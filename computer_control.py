import cv2
import mediapipe as mp
import pyautogui
import time
import math

from pycaw.pycaw import AudioUtilities


# ==========================================
# WINDOWS VOLUME CONTROL
# ==========================================

devices = AudioUtilities.GetSpeakers()
volume = devices.EndpointVolume


# ==========================================
# SCREEN SIZE
# ==========================================

screen_width, screen_height = pyautogui.size()

print("Screen size:", screen_width, "x", screen_height)


# ==========================================
# WEBCAM
# ==========================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Could not open webcam")
    exit()


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
# TIMERS
# ==========================================

last_click_time = 0
CLICK_COOLDOWN = 1.0

last_scroll_time = 0
SCROLL_COOLDOWN = 0.05

last_volume_time = 0
VOLUME_COOLDOWN = 0.5


# ==========================================
# CONTROL MODE
# ==========================================

control_enabled = False


# ==========================================
# DISTANCE FUNCTION
# ==========================================

def distance(p1, p2):

    return math.sqrt(
        (p1.x - p2.x) ** 2 +
        (p1.y - p2.y) ** 2
    )


# ==========================================
# FINGER STATE DETECTION
# ==========================================

def get_finger_states(landmarks):

    # Four fingers
    index_open = landmarks[8].y < landmarks[6].y

    middle_open = landmarks[12].y < landmarks[10].y

    ring_open = landmarks[16].y < landmarks[14].y

    pinky_open = landmarks[20].y < landmarks[18].y


    # Thumb
    thumb_tip = landmarks[4]

    thumb_ip = landmarks[3]

    thumb_mcp = landmarks[2]


    # Distance from thumb tip to palm
    thumb_tip_distance = distance(
        thumb_tip,
        landmarks[9]
    )


    # Distance from thumb base to palm
    thumb_mcp_distance = distance(
        thumb_mcp,
        landmarks[9]
    )


    # Improved thumb detection
    thumb_open = (
        thumb_tip_distance >
        thumb_mcp_distance * 1.15
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

def detect_gesture(landmarks):

    (
        thumb,
        index,
        middle,
        ring,
        pinky
    ) = get_finger_states(landmarks)


    # ======================================
    # FIST
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
    # THUMBS UP
    # ======================================

    if (
        thumb
        and not index
        and not middle
        and not ring
        and not pinky
    ):

        if landmarks[4].y < landmarks[3].y:

            return "THUMBS UP"


    # ======================================
    # VICTORY
    # ======================================

    if (
        index
        and middle
        and not ring
        and not pinky
    ):

        return "VICTORY"


    # ======================================
    # INDEX
    # ======================================

    if (
        index
        and not middle
        and not ring
        and not pinky
    ):

        return "INDEX"


    # ======================================
    # OPEN HAND
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
# STARTUP
# ==========================================

print()
print("🤖 AI Computer Control")
print()
print("Starting in 5 seconds...")
print("Keep your hand away from the camera.")
print()

for i in range(5, 0, -1):

    print(i)

    time.sleep(1)


print()
print("🚀 AI Computer Control Started!")
print()
print("☝️ INDEX      = Move Mouse")
print("👍 THUMBS UP  = Left Click")
print("✌️ VICTORY    = Scroll")
print("✋ OPEN HAND  = Volume Up")
print("✊ FIST       = Stop")
print()
print("⌨️ Press C = Control ON/OFF")
print("⌨️ Press Q = Quit")
print()
print("🔴 Control is currently OFF")
print()


# ==========================================
# MAIN LOOP
# ==========================================

while True:

    success, frame = cap.read()

    if not success:

        print("❌ Could not read camera frame.")

        break


    # Mirror camera
    frame = cv2.flip(frame, 1)


    # Convert BGR → RGB
    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )


    # MediaPipe
    results = hands.process(rgb_frame)


    gesture = "NO HAND"


    # ======================================
    # HAND DETECTED
    # ======================================

    if results.multi_hand_landmarks:

        hand_landmarks = results.multi_hand_landmarks[0]

        landmarks = hand_landmarks.landmark


        # Draw landmarks
        mp_draw.draw_landmarks(
            frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS
        )


        # Detect gesture
        gesture = detect_gesture(landmarks)


        # ==================================
        # COMPUTER ACTIONS
        # ONLY WHEN CONTROL IS ON
        # ==================================

        if control_enabled:


            # --------------------------------
            # INDEX → MOVE MOUSE
            # --------------------------------

            if gesture == "INDEX":

                index_tip = landmarks[8]

                mouse_x = int(
                    index_tip.x * screen_width
                )

                mouse_y = int(
                    index_tip.y * screen_height
                )

                pyautogui.moveTo(
                    mouse_x,
                    mouse_y,
                    duration=0.03
                )


            # --------------------------------
            # THUMBS UP → LEFT CLICK
            # --------------------------------

            elif gesture == "THUMBS UP":

                current_time = time.time()

                if (
                    current_time - last_click_time
                    > CLICK_COOLDOWN
                ):

                    pyautogui.click()

                    last_click_time = current_time

                    print("🖱️ LEFT CLICK")


            # --------------------------------
            # VICTORY → SCROLL
            # --------------------------------

            elif gesture == "VICTORY":

                current_time = time.time()

                if (
                    current_time - last_scroll_time
                    > SCROLL_COOLDOWN
                ):

                    index_tip = landmarks[8]


                    # Hand near top → Scroll UP

                    if index_tip.y < 0.35:

                        pyautogui.scroll(12)


                    # Hand near bottom → Scroll DOWN

                    elif index_tip.y > 0.65:

                        pyautogui.scroll(-12)


                    last_scroll_time = current_time


            # --------------------------------
            # OPEN HAND → VOLUME UP
            # --------------------------------

            elif gesture == "OPEN HAND":

                current_time = time.time()

                if (
                    current_time - last_volume_time
                    > VOLUME_COOLDOWN
                ):

                    current_volume = (
                        volume.GetMasterVolumeLevelScalar()
                    )


                    new_volume = min(
                        current_volume + 0.05,
                        1.0
                    )


                    volume.SetMasterVolumeLevelScalar(
                        new_volume,
                        None
                    )


                    last_volume_time = current_time


                    print(
                        "🔊 Volume:",
                        round(new_volume * 100),
                        "%"
                    )


            # --------------------------------
            # FIST → STOP
            # --------------------------------

            elif gesture == "FIST":

                pass


    # ======================================
    # DISPLAY GESTURE
    # ======================================

    cv2.putText(
        frame,
        "Gesture: " + gesture,
        (20, 45),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 0),
        2
    )


    # ======================================
    # DISPLAY CONTROL STATUS
    # ======================================

    if control_enabled:

        status_text = "CONTROL: ON"

    else:

        status_text = "CONTROL: OFF"


    cv2.putText(
        frame,
        status_text,
        (20, 85),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )


    # ======================================
    # INSTRUCTIONS
    # ======================================

    cv2.putText(
        frame,
        "C = ON/OFF | Q = Quit",
        (20, 125),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )


    # ======================================
    # SHOW WINDOW
    # ======================================

    cv2.imshow(
        "AI Computer Control",
        frame
    )


    # ======================================
    # KEYBOARD CONTROLS
    # ======================================

    key = cv2.waitKey(1) & 0xFF


    # C → Toggle control

    if key == ord("c"):

        control_enabled = not control_enabled


        if control_enabled:

            print()
            print("🟢 CONTROL ON")
            print("Computer control is ACTIVE.")
            print()

        else:

            print()
            print("🔴 CONTROL OFF")
            print("Computer control is PAUSED.")
            print()


    # Q → Quit

    elif key == ord("q"):

        break


# ==========================================
# CLEANUP
# ==========================================

cap.release()

hands.close()

cv2.destroyAllWindows()

print()
print("🛑 AI Computer Control stopped.")
