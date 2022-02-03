from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
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

api_key = '' # type your google stt api key
api_url = 'https://speech.googleapis.com/v1/speech:recognize?alt=json&key=' + api_key

@google_stt_app.post('/google_stt_file/')
async def google_stt_api(config: dict, file: File):
    UPLOAD_DIRECTORY = './'
    contents = await file.read()

    config = {'encoding': config['encoding'],  # wav
              'sample_rate_hertz': config['sample_rate_hertz'],
              'language_code': config['language_code'],
              }
    if type(file) is not bytes: # in case, file is wav file
        audio = {'content': base64.b64encode(file).decode('utf-8')}
    else: # file is base64
        audio = {'content': file.decode('utf-8')}

    payload = {
        'config': config,
        'audio': audio
    }

    response = requests.post(api_url, json.dumps(payload))

    response = response.json()

    result_string = ''

    try:
        for result in response['results']:
            result_string += result['alternatives'][0]['transcript']

        return result_string
    except Exception as e:
        return e