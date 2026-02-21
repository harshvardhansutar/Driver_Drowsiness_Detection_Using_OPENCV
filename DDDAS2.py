import cv2
import numpy as np
import dlib
from scipy.spatial import distance as dist
from pygame import mixer
import pyttsx3
from twilio.rest import Client
import time
import requests

# ----------------------------
# Driver Name
# ----------------------------
DRIVER_NAME = "Harshvardhan"

# ----------------------------
# Twilio Setup
# ----------------------------
account_sid = "YOUR_TWILIO_SID"
auth_token = "YOUR_TWILIO_TOKEN"

client = Client(account_sid, auth_token)

# ----------------------------
# Voice Engine
# ----------------------------
engine = pyttsx3.init()
voice_alert_played = False

# ----------------------------
# Location Function
# ----------------------------
def get_live_location():
    try:
        response = requests.get("https://ipinfo.io/json")
        data = response.json()
        return data.get("loc", "Location unavailable")
    except:
        return "Location unavailable"

# ----------------------------
# Send SMS Alert
# ----------------------------
def send_sms_alert():
    try:
        location = get_live_location()

        message = f"Drowsiness Alert! Driver:{DRIVER_NAME} Location:{location} Time:{time.strftime('%H:%M')}"

        client.messages.create(
            to='+919022890258',
            from_='+19789136557',
            body=message
        )

        print("SMS Sent!")

    except Exception as e:
        print("SMS Error:", e)


# ----------------------------
# EAR Function
# ----------------------------
def eye_aspect_ratio(eye):

    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])

    return (A + B) / (2.0 * C)


# ----------------------------
# MAR Function
# ----------------------------
def mouth_aspect_ratio(mouth):

    A = dist.euclidean(mouth[1], mouth[7])
    B = dist.euclidean(mouth[2], mouth[6])
    C = dist.euclidean(mouth[3], mouth[5])
    D = dist.euclidean(mouth[0], mouth[4])

    return (A + B + C) / (2.0 * D)


# ----------------------------
# Load Models
# ----------------------------
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# ----------------------------
# Parameters
# ----------------------------
EAR_THRESHOLD = 0.25
CONSEC_FRAMES = 20

MAR_THRESHOLD = 0.6
YAWN_FRAMES = 15

SMS_COOLDOWN = 120

# ----------------------------
# Variables
# ----------------------------
counter = 0
yawn_counter = 0
attention_counter = 0

alarm_on = False
drowsiness_detected = False
last_sms_time = 0

prev_time = 0

# ----------------------------
# Alarm Setup
# ----------------------------
mixer.init()
mixer.music.load("beep-02.wav")

# ----------------------------
# Camera
# ----------------------------
cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame,(640,480))
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    faces = detector(gray)

    # ----------------------------
    # FPS
    # ----------------------------
    current_time=time.time()
    fps=int(1/(current_time-prev_time)) if prev_time!=0 else 0
    prev_time=current_time

    # ----------------------------
    # Brightness Detection (Night Mode)
    # ----------------------------
    brightness=np.mean(gray)

    mode="DAY"
    if brightness<70:
        mode="NIGHT"

    if len(faces)==0:
        counter=0
        yawn_counter=0
        attention_counter=0

        if alarm_on:
            mixer.music.stop()
            alarm_on=False
            voice_alert_played=False


    for face in faces:

        landmarks = predictor(gray,face)

        left_eye=[]
        right_eye=[]
        mouth=[]

        for n in range(36,42):
            left_eye.append((landmarks.part(n).x,
                             landmarks.part(n).y))

        for n in range(42,48):
            right_eye.append((landmarks.part(n).x,
                              landmarks.part(n).y))

        for n in range(60,68):
            mouth.append((landmarks.part(n).x,
                          landmarks.part(n).y))


        ear=(eye_aspect_ratio(left_eye)+
             eye_aspect_ratio(right_eye))/2

        mar=mouth_aspect_ratio(mouth)


        # Draw Landmarks
        cv2.polylines(frame,[np.array(left_eye)],True,(0,255,0),1)
        cv2.polylines(frame,[np.array(right_eye)],True,(0,255,0),1)
        cv2.polylines(frame,[np.array(mouth)],True,(255,0,0),1)


        # ----------------------------
        # Attention Detection
        # ----------------------------
        face_center=(face.left()+face.right())//2
        frame_center=320

        if abs(face_center-frame_center)>120:
            attention_counter+=1
        else:
            attention_counter=0


        # ----------------------------
        # Eye Detection
        # ----------------------------
        if ear<EAR_THRESHOLD:
            counter+=1
        else:
            counter=0


        # ----------------------------
        # Yawn Detection
        # ----------------------------
        if mar>MAR_THRESHOLD:
            yawn_counter+=1
        else:
            yawn_counter=0


        # ----------------------------
        # Trigger Alarm
        # ----------------------------
        if counter>=CONSEC_FRAMES or yawn_counter>=YAWN_FRAMES:

            if not alarm_on:

                mixer.music.play(-1)
                alarm_on=True
                drowsiness_detected=True

                if not voice_alert_played:
                    engine.say("Warning driver is drowsy")
                    engine.runAndWait()
                    voice_alert_played=True


        # ----------------------------
        # Stop Alarm
        # ----------------------------
        if counter==0 and yawn_counter==0:

            if alarm_on:

                mixer.music.stop()
                alarm_on=False
                voice_alert_played=False


        # ----------------------------
        # UI STATUS
        # ----------------------------
        status="NORMAL" if not alarm_on else "DROWSY"
        eye_status="OPEN" if counter==0 else "CLOSED"
        yawn_status="NO" if yawn_counter==0 else "YES"


        # Alert Bar
        if alarm_on:
            cv2.rectangle(frame,(0,0),(640,60),(0,0,255),-1)

            cv2.putText(frame,
                        "DROWSINESS ALERT!",
                        (150,40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255,255,255),
                        3)


        # Attention Warning
        if attention_counter>30:

            cv2.putText(frame,
                        "LOOKING AWAY!",
                        (200,200),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (0,0,255),
                        3)


        # ----------------------------
        # Top Info
        # ----------------------------
        cv2.putText(frame,f"Driver: {DRIVER_NAME}",(10,80),
                    cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)

        cv2.putText(frame,f"FPS: {fps}",(540,80),
                    cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)


        # Mode Display
        cv2.putText(frame,f"Mode: {mode}",(500,110),
                    cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,255),2)


        # Status Text
        cv2.putText(frame,f"Status: {status}",(10,110),
                    cv2.FONT_HERSHEY_SIMPLEX,0.8,
                    (0,255,0) if status=="NORMAL" else (0,0,255),2)

        cv2.putText(frame,f"Eyes: {eye_status}",(10,140),
                    cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,255,0),2)

        cv2.putText(frame,f"Yawn: {yawn_status}",(10,170),
                    cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,0,0),2)


        # Bottom Dashboard
        cv2.rectangle(frame,(0,420),(640,480),(40,40,40),-1)

        cv2.putText(frame,f"EAR:{ear:.2f}",(50,455),
                    cv2.FONT_HERSHEY_SIMPLEX,0.8,(0,255,0),2)

        cv2.putText(frame,f"MAR:{mar:.2f}",(300,455),
                    cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0),2)


    # ----------------------------
    # SMS Cooldown
    # ----------------------------
    if drowsiness_detected:

        if time.time()-last_sms_time>SMS_COOLDOWN:

            send_sms_alert()
            last_sms_time=time.time()

        drowsiness_detected=False


    cv2.imshow("Driver Monitoring System",frame)

    if cv2.waitKey(1)&0xFF==ord('q'):
        break


cap.release()
cv2.destroyAllWindows()