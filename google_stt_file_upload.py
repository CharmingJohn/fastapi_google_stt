from fastapi import FastAPI, File, UploadFile, Form
from pydantic import BaseModel
import logging
import logging.handlers
import re
import base64
import requests
import json
import time
import os

LOG_FORMAT = '[%(asctime)-10s] (%(filename)s: %(levelname)s %(threadName)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger('fastapi_drill_2')
logger.setLevel(logging.INFO)

google_stt_app = FastAPI()

api_key = '' # type your google stt api key
api_url = 'https://speech.googleapis.com/v1/speech:recognize?alt=json&key=' + api_key

@google_stt_app.post('/google_stt_file/')
async def google_stt_api(encoding: str = Form(...), sample_rate_hertz: int = Form(...), language_code: str = Form(...), audio_file: UploadFile = File(...)):

    config = {'encoding': encoding,  # wav
              'sample_rate_hertz': sample_rate_hertz,
              'language_code': language_code,
              }
    audio_file = await audio_file.read()
    audio = {'content': base64.b64encode(audio_file).decode('utf-8')}

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

        return {'stt_result': result_string}
    except Exception as e:
        return {'error': e}