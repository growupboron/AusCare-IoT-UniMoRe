import datetime
import os
import random
import sqlite3

from PIL import Image
import ST7735
import time

DB_PATH = 'instance/database.db'

# generates a list of all patients in the database
def get_all_patients():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("Select * FROM Patient")
    patients = c.fetchall()
    conn.close()
    patient_list = []
    for patient in patients:
        patient_list.append(Patient(*patient))
    del patients
    return patient_list


class Patient(object):
    def __init__(self, patient_id=1, name='Billy', age=10, people_counter=0, last_emotion=None, supervisor='Micheal', last_timestamp=None, admin='Micheal'):
        
        self.patient_id = patient_id
        self.name = name
        self.people_counter = people_counter
        self.supervisor = supervisor
        self.emotion = last_emotion
        self.admin = admin
        self.timestamp = last_timestamp
        # if _patient_id is in the database, load the people_counter from the database
        self.load()

        # We could define other metrics here, like the average emotion, etc.

    def __str__(self):
        return "Patient: " + str(self.patient_id) + " Name: " + str(self.name)

    def __repr__(self):
        return self.__str__()

    def load(self):
        con = sqlite3.connect(DB_PATH)
        c = con.cursor()
        # if the table patients does not exist, create it
        c.execute("CREATE TABLE IF NOT EXISTS Patient (id integer PRIMARY KEY, name text, "
                  "people_counter integer, supervisor text, emotion text, admin text, timestamp text)")
        c.execute("SELECT * FROM Patient WHERE id = ?", (self.patient_id,))
        row = c.fetchone()
        if row:
            self.name, self.people_counter, self.supervisor, self.emotion, self.admin, self.timestamp = row[1:]
            return
        else:
            # if _patient_id is not in the database, create a new patient with the _patient_id and age
            con = sqlite3.connect(DB_PATH)
            c = con.cursor()
            c.execute("Insert into Patient (name, people_counter, supervisor, emotion, admin, timestamp) "
                      "values (?, ?, ?, ?, ?, ?)", (self.name, self.people_counter, self.supervisor, self.emotion, self.admin, self.timestamp))
            con.commit()
            con.close()

    '''def update(self, emotion, timestamp):
        con = sqlite3.connect(DB_PATH)
        cursor = con.cursor()
        cursor.execute("UPDATE patients SET (people_counter, last_emotion, last_timestamp) = (?, ?, ?) WHERE id = ?",
                       (self.people_counter, emotion, timestamp, self.patient_id))
        con.commit()
        con.close()'''

    def mapper(self, emotion):
        self.people_counter += 1
        timestamp = datetime.datetime.now()
        emoji = ''
        # driver code for st7735 display
        disp = ST7735.ST7735(port=0, cs=0, dc=24, backlight=None, rst=25, width=80, height=160, rotation=90, invert=True) # Comment if not on RPi
        WIDTH = disp.width      # Comment if not on RPi
        HEIGHT = disp.height    # Comment if not on RPi

        if emotion == "happiness":
            emoji = '😃'
            img = Image.open("website/static/emojis/happy.png")
        elif emotion == "sadness":
            emoji = '😔'
            img = Image.open("website/static/emojis/sadness.png")
        elif emotion == "anger":
            emoji = '😠'
            img = Image.open("website/static/emojis/anger.png")
        elif emotion == "surprise":
            emoji = '😮'
            img = Image.open("website/static/emojis/surprise.png")
        elif emotion == "disgust":
            emoji = '🤮'
            img = Image.open("website/static/emojis/disgust.png")
        elif emotion == "fear":
            emoji = '😨'
            img = Image.open("website/static/emojis/fear.png")
        elif emotion == "neutral":
            emoji = '😑'
            img = Image.open("website/static/emojis/neutral.png")
            
        img = img.resize((WIDTH, HEIGHT)) # Comment if not on RPi
        #img.show()
        disp.display(img) # Comment if not on RPi
        img.save("website/static/images/lastemotion.png")
        #self.update(emotion, timestamp)
        time.sleep(1)
        #img.close()
        img = Image.open("website/static/emojis/off.png")
        disp.display(img)           # Comment if not on RPi
        return timestamp, emoji
