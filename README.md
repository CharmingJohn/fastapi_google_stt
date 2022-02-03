# google_stt with class, fastapi

## How to use

### 1. google_stt.py (stt rest api with class)
set your wav file (ex. bed_8k.wav)
```python
audio_file = open('bed_8k.wav', 'rb') # type your audio file source
```

type your google_stt api key
```python
api_key = '' # type your google stt api key
api_url = 'https://speech.googleapis.com/v1/speech:recognize?alt=json&key=' + api_key
```

run python
```python
python google_stt.py
```

### 2. google_stt_file_upload.py (stt rest api with class)