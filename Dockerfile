FROM python:3.9.10

WORKDIR /app
# RUN apt -y update

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY .  ./

CMD uvicorn google_stt_file_upload:google_stt_app --reload

EXPOSE 8000