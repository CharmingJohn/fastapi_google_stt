# google_stt with class

## hwo to use

set your wav file in line 17 (ex. bed_8k.wav)
```python
audio_file = open('bed_8k.wav', 'rb') # type your audio file source
```

type your google_stt api key in line 36
```python
api_key = '' # type your google stt api key
api_url = 'https://speech.googleapis.com/v1/speech:recognize?alt=json&key=' + api_key
```

run python
```python
python google_stt.py
```