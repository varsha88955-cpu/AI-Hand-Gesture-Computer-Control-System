# AI Hand Gesture Computer Control System

## Project Overview

The **AI Hand Gesture Computer Control System** is a Python-based computer vision project that allows users to control basic computer operations using hand gestures in front of a webcam.

This project uses OpenCV and MediaPipe to detect hand movements and identify different hand gestures in real time. Based on the recognized gesture, the system performs computer actions such as moving the mouse cursor, clicking, scrolling, and controlling system volume.

The main objective of this project is to make computer interaction easier and provide a touch-free way to control a computer.

## Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy
- PyAutoGUI
- PyCAW
- Webcam

## Features

- Real-time hand detection using a webcam.
- Hand landmark detection and tracking.
- Hand gesture recognition.
- Mouse cursor movement using hand gestures.
- Left mouse click.
- Screen scrolling.
- System volume control.
- Keyboard option to enable or disable computer controls.

## Gesture-to-Action Mapping

| Hand Gesture | Computer Action |
|---|---|
| ☝️ Index Finger | Move Mouse Cursor |
| 👍 Thumbs Up | Left Mouse Click |
| ✌️ Victory Sign | Scroll Up / Down |
| 🖐️ Open Palm | Increase Volume |
| ✊ Closed Fist | Stop Action |

## How the Project Works

The system works through the following steps:

1. **Webcam Input:** The webcam captures live video of the user's hand.
2. **Image Processing:** OpenCV reads and processes the video frames.
3. **Hand Detection:** MediaPipe detects the hand and identifies its landmarks.
4. **Gesture Recognition:** The system checks finger positions to identify the hand gesture.
5. **Computer Control:** Based on the detected gesture, Python libraries perform the corresponding computer action.

## Project File Structure

```text
AI-Hand-Gesture-Computer-Control-System/
│
├── gesture_detection_bcup.py
├── hand_detection.py
├── mouse_control.py
├── volume_test.py
├── webcam_test.py
├── requirements.txt
└── README.md
```

### Description of Python Files

- `gesture_detection_bcup.py` – Detects and recognizes hand gestures.
- `hand_detection.py` – Detects hands and tracks hand landmarks.
- `mouse_control.py` – Performs mouse-related computer controls.
- `volume_test.py` – Main program for gesture-based computer control and volume testing.
- `webcam_test.py` – Tests webcam functionality.
- `requirements.txt` – Contains the required Python libraries.

## Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/varsha88955-cpu/AI-Hand-Gesture-Computer-Control-System.git
```

### Step 2: Open the Project Folder

```bash
cd AI-Hand-Gesture-Computer-Control-System
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment (Windows)

```bash
venv\Scripts\activate
```

### Step 5: Install Required Libraries

```bash
pip install -r requirements.txt
```

### Step 6: Run the Main Program

```bash
python volume_test.py
```

Make sure your webcam is connected and accessible before running the program.

## Keyboard Controls

- Press `C` to enable or disable computer controls.
- Press `Q` to close the application.

Computer controls start in the OFF state for safety.

## Computer Vision Approach

This project uses MediaPipe Hands to detect hand landmarks from webcam frames. The detected landmarks represent important points on the fingers and palm.

The positions of these landmarks are analyzed to determine whether fingers are open or closed. Based on the finger positions, the system identifies gestures and connects them to specific computer operations.

OpenCV is used for webcam access and image processing, while PyAutoGUI and PyCAW are used to perform computer actions.

## Project Screenshots

Screenshots of the working project will be added here.

### Hand Detection
![Hand Detection](screenshots/01_hand_detection.png)

### Gesture Recognition
![Gesture Recognition](screenshots/02_gesture_detection.png)

### Mouse Control
![Mouse Control](screenshots/03_mouse_control.png)

### Volume Control
![Volume Control](screenshots/04_volume_control.png)

## Future Enhancements

- Add more hand gestures.
- Improve gesture recognition.
- Add additional computer control features.
- Improve cursor movement accuracy.
- Support more user-customizable actions.

## Conclusion

The AI Hand Gesture Computer Control System demonstrates how computer vision can be used to control computer operations through hand gestures. It combines Python, OpenCV, and MediaPipe to create a simple touch-free computer interaction system.

## Author

**Bhoompalli Varsha**

Computer Science Engineering (Cyber Security) Graduate

GitHub: [varsha88955-cpu](https://github.com/varsha88955-cpu)
