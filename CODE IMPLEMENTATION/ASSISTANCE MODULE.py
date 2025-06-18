import os
import csv
import time
import threading
from datetime import datetime
from io import BytesIO

import pandas as pd
from gtts import gTTS
from pygame import mixer

# Initialize mixer
mixer.init()

# Text-to-speech function
def speak(text):
    mp3file = BytesIO()
    tts = gTTS(text, lang="en", tld='us')
    tts.write_to_fp(mp3file)
    mp3file.seek(0)
    mixer.music.load(mp3file, "mp3")
    mixer.music.play()
    while mixer.music.get_busy():
        time.sleep(0.2)

# Reminder CSV file setup
reminder_file = "reminders.csv"
if not os.path.exists(reminder_file):
    with open(reminder_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time", "message"])
        # Add default reminders
        writer.writerow(["07:30", "Good morning! Time to take your thyroid medication."])
        writer.writerow(["08:00", "Breakfast time! Don't forget to take your multivitamin."])
        writer.writerow(["12:30", "Lunch time! Please take your blood pressure tablet."])
        writer.writerow(["15:00", "Afternoon dose! It's time for your eye drops."])
        writer.writerow(["18:00", "Evening medicine time! Please take your diabetes medication."])
        writer.writerow(["20:00", "Good evening! It's time for your cholesterol tablet."])
        writer.writerow(["21:30", "Bedtime! Take your sleeping pill if prescribed."])

# Function to check reminders

def reminder_loop():
    print("Reminder system started...")
    speak("Reminder system started")
    last_reminder_time = None

    while True:
        try:
            now = datetime.now().strftime("%H:%M")
            if now != last_reminder_time:
                df = pd.read_csv(reminder_file)
                for index, row in df.iterrows():
                    if row['time'] == now:
                        print(f"Reminder: {row['message']}")
                        speak(f"Reminder: {row['message']}")
                        last_reminder_time = now
                        break
            time.sleep(1)
        except KeyboardInterrupt:
            print("Reminder system stopped.")
            speak("Reminder system stopped")
            break

# Start reminder system in a thread
if __name__ == "__main__":
    reminder_thread = threading.Thread(target=reminder_loop)
    reminder_thread.daemon = True
    reminder_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program terminated by user.")
        speak("Program terminated by user.")
