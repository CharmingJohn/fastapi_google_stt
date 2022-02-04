from fastapi import FastAPI
import logging
import logging.handlers
import re
import base64
import requests
import json
import time

LOG_FORMAT = "[%(asctime)-10s] (%(filename)s:%(lineno)d) %(levelname)s %(threadName)s - %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger('google_stt')
logger.setLevel(logging.INFO)

file_handler = logging.handlers.TimedRotatingFileHandler(
        filename='./logs/google_stt_log', when='midnight', interval=1
        )
file_handler.suffix = '%Y%m%d'
logger.addHandler(file_handler)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

google_stt_app = FastAPI()

audio_file = open('bed_8k.wav', 'rb') # type your audio file source
data = audio_file.read()
audio_file.close()

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
        logger.info('payload: ', payload)

    def response_stt_api_rest(self):
        response = requests.post(api_url, json.dumps(self.payload))
        response = response.json()
        logger.info('response: ', response)

        final_result = ''

        try:
            for result in response['results']:
                print('Transcript: {}'.format(result['alternatives'][0]['transcript']))
                final_result += result['alternatives'][0]['transcript']
            logger.info('final_result: ', final_result)
            return final_result
        except Exception as e:
            print('error: ', e)
            logger.error('error : e')
            return e


test = google_stt(payload=payload)
test.response_stt_api_rest()
