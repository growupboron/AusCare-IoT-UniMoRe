import base64
import os
import time
from threading import Thread

import requests
from config import API_KEY, API_SECRET, API, DEBUG
import patient
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

def emotion_detect():
    while True:
        # real-time emotion detection with the R-Pi
        # Comment if not on RPi
        # take a photo
        take_photo()
        # encode the image
        with open('website/static/images/face.jpeg', 'rb') as image_file:
            encoded_image = encode_image(image_file.read())
        # send the image to the API and get the response
        response = requests.post(API, data={'api_key': API_KEY, 'api_secret': API_SECRET, 'image_base64': encoded_image},
                                 params={'return_attributes': 'emotion'})
        faceID = emotions = response.json().get('faces')[0].get('face_token') #Used for number of people met
        emotions = response.json().get('faces')[0].get('attributes').get('emotion')
        emotion, emoticon = emotion_mapper(pat, emotions)
        #print(response.json())
        print(f'timestamp: {emoticon[0]}, Emotion: {emotion}, Emoji: {emoticon[1]}, FaceID: {faceID}')

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

try:
    while True:
        pat = Patient(1, 'Billy', 10, 0, None, None)
        pat.load()
        image_urls = list()
        start = time.time()
        # encode the images in base64
        def encode_image(image):
            return base64.b64encode(image)

        encoded_images = []

        for file in os.listdir('website/static/images'):
            if file.endswith('.jpeg' or '.png' or '.jpg'):
                with open(os.path.join('images', file), 'rb') as image_file:
                    encoded_images.append(encode_image(image_file.read()))
        
except KeyboardInterrupt:
    print("Stopping...")
    print(f'\nEnded.\nTime of execution: {time.time() - start:.2} s')
    #if DEBUG: print(f'\nEnded.\nTime of execution: {time.time() - start:.2} s')
