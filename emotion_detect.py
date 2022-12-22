import base64
import os
import time
from threading import Thread

import requests
from config import API_KEY, API_SECRET, API, DEBUG
import patient
from patient import Patient


def emotion_mapper(pat, emotion_list):
    '''
    returns the emotion with the highest confidence
    '''
    return pat.mapper(max(emotion_list, key=emotion_list.get))


'''def take_photo():
    # take a photo with the camera
    # camera = cv2.VideoCapture(0) # for testing purposes
    camera = PiCamera()
    camera.start_preview()
    camera.resolution = (640, 480)
    camera.capture('images/face.jpeg')
    time.sleep(15)'''


def emotion_detect():
    while True:
        # real-time emotion detection with the R-Pi
        '''# take a photo
        take_photo()
        # encode the image
        with open('images/face.jpeg', 'rb') as image_file:
            encoded_image = encode_image(image_file.read())
        # send the image to the API and get the response
        response = requests.post(API, data={'api_key': API_KEY, 'api_secret': API_SECRET, 'image_base64': encoded_image},
                                 params={'return_attributes': 'emotion'})
        emotions = response.json().get('faces')[0].get('attributes').get('emotion')
        emoticon = emotion_mapper(pat, emotions)
        print(f'timestamp: {emoticon[0]}, Emoji: {emoticon[1]}')'''

        # for testing purposes
        for image in encoded_images:
            response = requests.post(API, data={'api_key': API_KEY, 'api_secret': API_SECRET, 'image_base64': image},
                                     params={'return_attributes': 'emotion'})
            if DEBUG:
                print(response.json())
            # get only the emotions data for the first face detected

            emotions = response.json().get('faces')[0].get('attributes').get('emotion')
            emoticon = emotion_mapper(pat, emotions)
            print(f'timestamp: {emoticon[0]}, Emoji: {emoticon[1]}')
            #time.sleep(5)


# Some photos to test with
thread = Thread(target=emotion_detect)

pat = Patient(1, 'Billy', 10, 0, None, None)
pat.load()
image_urls = list()
start = time.time()


# encode the images in base64
def encode_image(image):
    return base64.b64encode(image)


encoded_images = []
for file in os.listdir('images'):
    if file.endswith('.jpeg' or '.png' or '.jpg'):
        with open(os.path.join('images', file), 'rb') as image_file:
            encoded_images.append(encode_image(image_file.read()))
thread.start()
#if DEBUG: print(f'\nEnded.\nTime of execution: {time.time() - start:.2} s')
