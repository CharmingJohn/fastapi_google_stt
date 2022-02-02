from fastapi import FastAPI
import logging
import logging.handlers
import re
import base64
import requests

LOG_FORMAT = '[%(asctime)-10s] (%(filename)s: %(levelname)s %(threadName)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger('fastapi_drill_2')
logger.setLevel(logging.INFO)

audio_file = '' # type your audio file source

config = {'encoding': 'LINEAR16',
          'sample_rate_hertz': 8000,
          'language_code': 'en-US',
          'content': 'input_audio'
          }


api_key = '' # btype your google stt api key
api_url = 'https://speech.googleapis.com/v1/speech:recognize?key=' + api_key



class google_stt:
    def __init__(self, config, audio):
        self.config = config
        self.audio = audio

    def response_stt_api(self):
        response = requests.post(api_url, self.config, self.audio)