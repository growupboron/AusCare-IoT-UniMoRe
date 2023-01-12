import base64
import os
import sqlite3
import time

from threading import Thread

import numpy as np

from flask import g, session
import requests
from config import API_KEY, API_SECRET, API, DEBUG

from patient import Patient
import cv2

from picamera import PiCamera                           # Comment if not on RPi

def emotion_mapper(pat, emotion_list):
    '''
    returns the emotion and emoji with the highest confidence
    '''
    emotion = max(emotion_list, key=emotion_list.get)
    return emotion, pat.mapper(emotion)

def take_photo():
    # take a photo with the camera
    camera = PiCamera()
    camera.resolution = (640, 480) # need a well lit room
    camera.start_preview()
    time.sleep(1)
    # vertically flipping image as PiCam is mounted invertly
    camera.capture('website/static/images/face_flipped.jpeg') 
    camera.close()
    capture = cv2.imread('website/static/images/face_flipped.jpeg')
    capture = cv2.flip(capture,0)
    cv2.imwrite('website/static/images/face.jpeg', capture)

# class EmotionThread(Thread):
    # def __init__(self):
        # Thread.__init__(self)
        # self.timestamp = None
        # self.emotion = None
        # self.emoji = None
        # self.faceID = None

    # def run(self):
        # while True:
            # # real-time emotion detection with the R-Pi
            # # Comment if not on RPi
            # # take a photo
            # take_photo()
            # # encode the image
            # with open('website/static/images/face.jpeg', 'rb') as image_file:
                # encoded_image = encode_image(image_file.read())
            # # send the image to the API and get the response
            # response = requests.post(API, data={'api_key': API_KEY, 'api_secret': API_SECRET, 'image_base64': encoded_image},
                                     # params={'return_attributes': 'emotion'})
            # faceID = response.json().get('faces')[0].get('face_token') #Used for number of people met
            # emotions = response.json().get('faces')[0].get('attributes').get('emotion')
            # emotion, emoticon = emotion_mapper(pat, emotions)
            # #print(response.json())
            # #print(f'timestamp: {emoticon[0]}, Emotion: {emotion}, Emoji: {emoticon[1]}, FaceID: {faceID}')
            # timestamp = emoticon[0]
            # emoji = emoticon[1]
            # #print(response.json())
            # print(f'timestamp: {timestamp}, Emotion: {emotion}, Emoji: {emoji}, FaceID: {faceID}')
            # sleep(1)
            # self.timestamp = timestamp
            # self.emotion = emotion
            # self.emoji = emoji
            # self.faceID = faceID
            # print (self.timestamp)
            # #return timestamp, emotion, emoji, faceID

def emotion_detect():
    while True:
        # real-time emotion detection with the R-Pi
        # Comment if not on RPi
        global timestamp, emotion, emoji, faceID
        # take a photo
        take_photo()
        # encode the image
        with open('website/static/images/face.jpeg', 'rb') as image_file:
            encoded_image = encode_image(image_file.read())
        # send the image to the API and get the response
        response = requests.post(API, data={'api_key': API_KEY, 'api_secret': API_SECRET, 'image_base64': encoded_image},
                                 params={'return_attributes': 'emotion'})
        faceID = response.json().get('faces')[0].get('face_token') #Used for number of people met
        emotions = response.json().get('faces')[0].get('attributes').get('emotion')
        emotion, emoticon = emotion_mapper(pat, emotions)
        #print(response.json())
        #print(f'timestamp: {emoticon[0]}, Emotion: {emotion}, Emoji: {emoticon[1]}, FaceID: {faceID}')
        timestamp = emoticon[0]
        emoji = emoticon[1]
        #print(response.json())

        # getting the enoji image for the guessed emotion
        with open(os.path.join('website/static/images', emotion), 'rb') as emoji_img:
            encoded_emoji_img = encode_image(emoji_img.read())

        # save infotmations to the database
        con = sqlite3.connect('website/database.db')
        cur = con.cursor()
        cur.execute("INSERT INTO Patient (user_id, name, people_counter, timestamp,  photo, emotion, emoji, supervisor, admin, evaluation, face_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",(pat.patient_id, pat.name, pat.people_counter+1, timestamp, encoded_image, emotion, encoded_emoji_img, pat.supervisor, pat.admin, np.random.choice(['good', 'bad']), faceID))
        con.commit()
        con.close()
        # db.session.add(Patient(user_id=pat.patient_id, name=pat.name, timestamp=timestamp, photo=encoded_image, emotion=emotion, emoji=encoded_emoji_img, supervisor=pat.supervisor, admin=pat.admin, evaluation='good', face_id=faceID))
        print(f'timestamp: {timestamp}, Emotion: {emotion}, Emoji: {emoji}, FaceID: {faceID}')

        #data = timestamp, emotion, emoji, faceID
        #with open('website/static/buffer.txt','w') as f:
            #f.write(str(data))
        #return timestamp, emotion, emoji, faceID

        '''
        # for testing purposes w/o picam
        for image in encoded_images:
            response = requests.post(API, data={'api_key': API_KEY, 'api_secret': API_SECRET, 'image_base64': image},
                                     params={'return_attributes': 'emotion'})
            if DEBUG:
                print(response.json())
            # get only the emotions data for the first face detected

            faceID = emotions = response.json().get('faces')[0].get('face_token') #Used for number of people met
            emotions = response.json().get('faces')[0].get('attributes').get('emotion')
            emotion, emoticon = emotion_mapper(pat, emotions)
            print(f'timestamp: {emoticon[0]}, Emotion: {emotion}, Emoji: {emoticon[1]}, FaceID: {faceID}')
            #time.sleep(5)
        '''

thread = Thread(target=emotion_detect)
thread.start()

# thread = EmotionThread()
# thread.start()

try:
    while True:
        if g and g.role == 'User':
            pat = Patient(patient_id=g.id, name=g.first_name)
        else:
            # dummy patient to avod the application to crash, in the future  we can just retrieve the last user in the database if no user is logged in
            pat = Patient(1, 'Billy', 0)
        pat.load()
        image_urls = list()
        start = time.time()
        # encode the images in base64
        def encode_image(image):
            return base64.b64encode(image)
        encoded_images = []
        for file in os.listdir('website/static/images'):
            if file.endswith('.jpeg' or '.png' or '.jpg'):
                with open(os.path.join('website/static/images', file), 'rb') as image_file:
                    encoded_images.append(encode_image(image_file.read()))
                            
except KeyboardInterrupt:
    print("Stopping...")
    print(f'\nEnded.\nTime of execution: {time.time() - start:.2} s')
    #if DEBUG: print(f'\nEnded.\nTime of execution: {time.time() - start:.2} s')
