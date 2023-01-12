import base64
import os
import time

import requests

import patient
from patient import Patient

'''
Simple script to test Face++ API
'''

API_KEY = 'h0w3FvaxU8hDq9WqFIVxmZPM2rcqARaw'
API_SECRET = 'O1PFTAa0-aL6twhn5Cnbr7_XPIdbUzQZ'
API = 'https://api-us.faceplusplus.com/facepp/v3/detect'
DEBUG = True  # set to false later
pat = Patient(1, 'Billy', 10, 0, None, None)
pat.load()


# camera = PiCamera()
# webcam = cv2.VideoCapture(0)
def emotion_mapper(emotion_list):
    '''
    returns the emotion with the highest confidence
    '''
    return pat.mapper(max(emotion_list, key=emotion_list.get))


# Some photos to test with
image_urls = list()
start = time.time()
print('Testing Face++ API..')

# encode the images in base64
encoded_images = []
for file in os.listdir('../../images'):
    if file.endswith('.jpeg' or '.png' or '.jpg'):
        with open(os.path.join('../../images', file), 'rb') as image_file:
            encoded_images.append(base64.b64encode(image_file.read()))


for image in encoded_images:
    response = requests.post(API, data={'api_key': API_KEY, 'api_secret': API_SECRET, 'image_base64': image},
                             params={'return_attributes': 'emotion'})
    if DEBUG:
        print(response.json())
        #print({f'face #{i}': face.get('attributes').get('emotion') for i, face in
        #       enumerate(response.json().get('faces'))},
        #      end=' ---> ')
    # get only the emotions data for the first face detected

    emotions = response.json().get('faces')[0].get('attributes').get('emotion')
    emoticon = emotion_mapper(emotions)
    print(f'timestamp: {emoticon[0]}, Emoji: {emoticon[1]}' )

print(patient.get_all_patients())
if DEBUG: print(f'\nEnded.\nTime of execution: {time.time() - start:.2} s')
