import requests

'''
Simple script to test Face++ API
'''

API_KEY = 'h0w3FvaxU8hDq9WqFIVxmZPM2rcqARaw'
API_SECRET = 'O1PFTAa0-aL6twhn5Cnbr7_XPIdbUzQZ'

API = 'https://api-us.faceplusplus.com/facepp/v3/detect'
image_url = 'https://img.freepik.com/premium-photo/cute-caucasian-child-little-boy-smile-make-happy-face-human-emotions-children_183219-8827.jpg?w=2000'
# make a post request to API
response = requests.post(API, data={'api_key': API_KEY, 'api_secret': API_SECRET, 'image_url': image_url}, params={'return_attributes':'emotion'})
print(response.json())
