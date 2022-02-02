from fastapi import FastAPI
import logging
import logging.handlers
import re

LOG_FORMAT = '[%(asctime)-10s] (%(filename)s: %(levelname)s %(threadName)s - %(message)s'
logging.basicConfig(format=LOG_FORMAT)
logger = logging.getLogger('fastapi_drill_2')
logger.setLevel(logging.INFO)

