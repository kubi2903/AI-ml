import cv2
import numpy as np
import os
import time
from datetime import datetime
from io import BytesIO
from gtts import gTTS
from pygame import mixer
import face_recognition

# Initialize camera and mixer
cap = cv2.VideoCapture(0)
mixer.init()

# Path to training images
path = 'data'
stdImg = []
stdName = []
myList = os.listdir(path)

# Text-to-speech function
def text_to_speech_audio(text):
    mp3file = BytesIO()
    tts = gTTS(text, lang="en", tld="us")
    tts.write_to_fp(mp3file)
    mp3file.seek(0)
    try:
        mixer.music.load(mp3file, "mp3")
        mixer.music.play()
        while mixer.music.get_busy():
            time.sleep(0.2)
    except KeyboardInterrupt:
        mixer.music.stop()

# Load and encode known images
for cl in myList:
    curimg = cv2.imread(f'{path}/{cl}')
    stdImg.append(curimg)
    stdName.append(os.path.splitext(cl)[0])

studentName = [name.upper() for name in stdName]
s1 = s2 = s3 = s4 = s5 = 0

# Resize function
def resize(img, size):
    width = int(img.shape[1] * size)
    height = int(img.shape[0] * size)
    return cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

# Find encodings for known faces
def findEncoding(images):
    imgEncodings = []
    for img in images:
        img = resize(img, 0.50)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodeimg = face_recognition.face_encodings(img)[0]
        imgEncodings.append(encodeimg)
    return imgEncodings

EncodeList = findEncoding(stdImg)

# Main loop for recognition
while True:
    success, frame = cap.read()
    Smaller_frames = cv2.resize(frame, (0, 0), None, 0.25, 0.25)
    facesInFrame = face_recognition.face_locations(Smaller_frames)
    encodeFacesInFrame = face_recognition.face_encodings(Smaller_frames, facesInFrame)

    for encodeFace, faceloc in zip(encodeFacesInFrame, facesInFrame):
        matches = face_recognition.compare_faces(EncodeList, encodeFace)
        facedis = face_recognition.face_distance(EncodeList, encodeFace)
        matchIndex = np.argmin(facedis)

        if matches[matchIndex]:
            name = studentName[matchIndex].upper()
            y1, x2, y2, x1 = [v * 4 for v in faceloc]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
            cv2.rectangle(frame, (x1, y2 - 25), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            if name == 'RAZZAQ':
                s1 += 1
                if s1 >= 6:
                    text_to_speech_audio("RAZZAQ is detected - He is Student of B.TECH Final year")
                    s1 = s2 = s3 = s4 = s5 = 0
        else:
            y1, x2, y2, x1 = [v * 4 for v in faceloc]
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 3)
            cv2.putText(frame, 'INTRUDER', (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    cv2.imshow('Face Attendance System', frame)
    if cv2.waitKey(1) == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()
