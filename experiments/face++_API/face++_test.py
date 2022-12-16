import time

import requests

'''
Simple script to test Face++ API
'''

API_KEY = 'h0w3FvaxU8hDq9WqFIVxmZPM2rcqARaw'
API_SECRET = 'O1PFTAa0-aL6twhn5Cnbr7_XPIdbUzQZ'
API = 'https://api-us.faceplusplus.com/facepp/v3/detect'


def emotion_mapper(emotions):
    '''
    returns the emotion with the highest confidence
    '''
    return max(emotions, key=emotions.get)


# Some photos to test with
image_urls = [
'https://thumbs.dreamstime.com/z/young-happy-people-have-fun-outdoors-autumn-fiendship-concept-smiling-friends-communication-weekend-university-123724503.jpg',
'https://img.freepik.com/free-photo/people-emotions-lifestyle-fashion-concept-depressed-sad-gloomy-korean-girl-pouting-looking-down-dumps-feeling-upset-displeased-standing-yellow-background_1258-58873.jpg',
'https://img.freepik.com/free-photo/smiling-happy-boy-pointing-fingers-up-copyspace_171337-16394.jpg?w=1480&t=st=1671222856~exp=1671223456~hmac=309a702cb5fc2a0729cafc34db393402eb8e351bfce4b85192355a306376c78d',
'https://img.freepik.com/free-photo/furious-angry-european-man-clenches-teeth-fists-with-rage-tries-control-his-negative-emotions_273609-16747.jpg?w=1480&t=st=1671221747~exp=1671222347~hmac=6ca368ede10b77856a49c51a9faff8cc7baf73b1b89d7851a19eaf123220d3a1',
'https://previews.123rf.com/images/kurhan/kurhan1703/kurhan170300142/73292807-girl-disgusted-face-expression.jpg',
'https://img.freepik.com/free-photo/senior-man-black-tee-portrait_53876-129945.jpg?w=1480&t=st=1671221878~exp=1671222478~hmac=c3b27f53250760966d44c9f59e99377f5bdf0cdb50817c2b99ac31cc5badd2cb',
'https://media.istockphoto.com/id/527879691/it/foto/paura-uomo.jpg?s=612x612&w=is&k=20&c=-ojjxqOe8hDae9zawJTDO1CcvmDppTk6NYffavidvug='
]
print('Testing Face++ API..')
# make a post request to the API
start = time.time()
for image_url in image_urls:
    response = requests.post(API, data={'api_key': API_KEY, 'api_secret': API_SECRET, 'image_url': image_url}, params={'return_attributes':'emotion'})
    print({f'face #{i}': face.get('attributes').get('emotion') for i, face in enumerate(response.json().get('faces'))},
          end=' ---> ')
    # get only the emotions data for the first face detected

    emotions = response.json().get('faces')[0].get('attributes').get('emotion')
    print(f'Emotion: {emotion_mapper(emotions)}',)

print(f'\nEnded.\nTime of execution: {time.time()-start:.2} s')