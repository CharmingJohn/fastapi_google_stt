from fastapi import FastAPI
import logging
import logging.handlers
import re
import base64
import requests
import json
import time

LOG_FORMAT = '[%(asctime)-10s] (%(filename)s: %(levelname)s %(threadName)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger('fastapi_drill_2')
logger.setLevel(logging.INFO)

google_stt_app = FastAPI()

audio_file = open('bed_8k.wav', 'rb') # type your audio file source
data = audio_file.read()

config = {'encoding': 'LINEAR16', # wav
          'sample_rate_hertz': 8000,
          'language_code': 'en-US',
          }

audio = {'content': base64.b64encode(data).decode('utf-8')}

payload= {
    'config': config,
    'audio': audio
}

api_key = '' # type your google stt api key
api_url = 'https://speech.googleapis.com/v1/speech:recognize?alt=json&key=' + api_key

class google_stt:
    def __init__(self, payload):
        self.payload = payload

    def response_stt_api_rest(self):
        response = requests.post(api_url, json.dumps(self.payload))

        response = response.json()

        try:
            for result in response['results']:
                print('Transcript: {}'.format(result['alternatives'][0]['transcript']))
        except Exception as e:
            print('error: ', e)

'''
@google_stt_app.get('/')
async def landing_page():
    return 'visit /google_stt/'

@google_stt_app.post('/google_stt/')
async def google_stt_api(payload):
    test = google_stt(payload=payload)
    result = test.response_stt_api_rest()

    return result
'''

test = google_stt(payload=payload)
test.response_stt_api_rest()
