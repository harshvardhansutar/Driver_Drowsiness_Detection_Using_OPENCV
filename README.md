# Driver Drowsiness Detection and Alert System (DDDAS)

## Overview

The **Driver Drowsiness Detection and Alert System (DDDAS)** is an intelligent real-time monitoring system that detects driver fatigue and distraction using computer vision and machine learning concepts.

The system uses a webcam to monitor the driver's face and analyzes **eye closure, yawning behavior, and attention level** to determine drowsiness. When fatigue is detected, the system activates an **audio alarm, voice warning, and SMS alert** to ensure driver safety.

This project aims to reduce road accidents caused by driver fatigue by providing early warnings and emergency notifications.

---

## Features

### Core Features

* Real-time driver monitoring using webcam
* Eye Drowsiness Detection using Eye Aspect Ratio (EAR)
* Yawn Detection using Mouth Aspect Ratio (MAR)
* Driver Attention Detection (Looking Away Detection)
* Automatic Alarm System
* Voice Warning System
* SMS Alert System

### Smart Features

* Night/Day Mode Detection
* Live Fatigue Indicators
* FPS (Performance Monitor)
* Driver Status Display
* Real-Time Dashboard UI
* Emergency Location SMS

### Safety Alerts

The system provides:

1. **Audio Alarm**

   * Continuous buzzer sound when drowsiness is detected.

2. **Voice Warning**

   * Spoken alert:

   ```
   Warning driver is drowsy
   ```

3. **SMS Notification**

   * Emergency SMS sent to registered mobile number with:
   * Driver name
   * Time
   * Approximate location

---

## Technologies Used

### Programming Language

* Python

### Libraries

* OpenCV – Computer vision processing
* Dlib – Facial landmark detection
* NumPy – Numerical operations
* SciPy – Distance calculations
* PyGame – Alarm sound system
* Pyttsx3 – Voice alert system
* Twilio – SMS alert system
* Requests – Location detection

---

## System Architecture

Camera → Face Detection → Eye & Mouth Analysis → Fatigue Detection → Alert System

Detection Layer:

* Eye Aspect Ratio (EAR)
* Mouth Aspect Ratio (MAR)
* Attention Detection
* Light Detection

Alert Layer:

* Audio Alarm
* Voice Warning
* SMS Alert

---

## Detection Methods

### Eye Aspect Ratio (EAR)

EAR measures eye openness using facial landmarks.

Low EAR value indicates closed eyes and possible drowsiness.

### Mouth Aspect Ratio (MAR)

MAR detects yawning by measuring mouth opening.

High MAR value indicates yawning behavior.

### Attention Detection

The system detects if the driver is looking away from the road for extended time.

### Night Mode Detection

Brightness level is analyzed to detect night driving conditions.

---

## Installation

### Step 1 – Install Python Libraries

Run:

```
pip install opencv-python
pip install numpy
pip install dlib
pip install scipy
pip install pygame
pip install pyttsx3
pip install twilio
pip install requests
```

---

### Step 2 – Download Landmark Model

Download:

```
shape_predictor_68_face_landmarks.dat
```

Place it in the project folder.

---

### Step 3 – Run Program

```
python main.py
```

---

## How It Works

1. Camera captures driver's face
2. Facial landmarks are detected
3. EAR and MAR values are calculated
4. System checks for:

* Eyes closed too long
* Yawning
* Looking away

5. If drowsiness detected:

* Alarm starts
* Voice warning plays
* SMS sent

---

## User Interface

The system displays:

* Driver Name
* FPS
* Driver Status
* Eye Status
* Yawn Status
* Day/Night Mode
* EAR Value
* MAR Value

Alert Mode shows:

```
DROWSINESS ALERT!
```

---

## Project Structure

```
DDDAS/
│
├── main.py
├── beep-02.wav
├── shape_predictor_68_face_landmarks.dat
└── README.md
```

---

## Applications

* Smart Vehicles
* Driver Safety Systems
* Fleet Monitoring
* Transportation Industry
* Research Projects

---

## Advantages

* Real-time monitoring
* Low cost solution
* Easy to implement
* Accurate fatigue detection
* Automatic emergency alert

---

## Limitations

* Requires proper lighting
* Requires camera positioning
* Works best with frontal face
* SMS requires internet connection

---

## Future Improvements

* Mobile App Integration
* Cloud Monitoring
* GPS Hardware Integration
* Deep Learning Eye Detection
* Driver Identification
* Fatigue Score System

---

## Author

**Harshvardhan Sutar**

Bachelor of Engineering – Computer Engineering
Ajeenkya DY Patil School of Engineering

---

## License

This project is for educational and research purposes.
