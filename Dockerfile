FROM tiangolo/uwsgi-nginx:python3.11

WORKDIR /simple_whisper_web

RUN apt-get update && apt-get install -y ffmpeg

COPY ./simple_whisper_web/requirements.txt /simple_whisper_web/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./simple_whisper_web /simple_whisper_web/

CMD ["gunicorn", "--conf", "/simple_whisper_web/gunicorn_conf.py", "--bind", "0.0.0.0:9999", "application:app"]
