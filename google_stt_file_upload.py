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
import aiohttp

LOG_FORMAT = "[%(asctime)-10s] (%(filename)s:%(lineno)d) %(levelname)s %(threadName)s - %(message)s"
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger('google_stt_file_upload')
logger.setLevel(logging.INFO)
if not os.path.exists('./logs'):
    os.mkdir('./logs')
file_handler = logging.handlers.TimedRotatingFileHandler(
        filename='./logs/google_stt_file_upload_log', when='midnight', interval=1
        )
file_handler.suffix = '%Y%m%d'
logger.addHandler(file_handler)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

google_stt_app = FastAPI()

api_key = '' # type your google stt api key
api_url = 'https://speech.googleapis.com/v1/speech:recognize?alt=json&key=' + api_key

@google_stt_app.post('/google_stt_file/')
async def google_stt_api(encoding: str = Form(...), sample_rate_hertz: int = Form(...), language_code: str = Form(...), audio_file: UploadFile = File(...)) -> dict:

    config = {'encoding': encoding,  # wav
              'sample_rated_hertz': sample_rate_hertz,
              'language_code': language_code,
              }
    audio_content = await audio_file.read()
    audio = {'content': base64.b64encode(audio_content).decode('utf-8')}

    payload = {
        'config': config,
        'audio': audio
    }
    logger.info('payload : {}, {}'.format(config, audio_file.filename))

    # response = requests.post(api_url, json.dumps(payload))
    async with aiohttp.ClientSession() as session:
        async with session.post(api_url, json.dumps(payload)) as response:
            response = await response.json()

    logger.info('response from google stt: {}'.format(response))

    result_string = ''

    try:
        for result in response['results']:
            result_string += result['alternatives'][0]['transcript']

        logger.info('result_string: {}'.format(result_string))
        return {'stt_result': result_string}
    except Exception as e:
        logger.error('error: {}'.format(e))
        return {'error': e}