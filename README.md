# Simple Whisper Webapp
This application is designed for older or less tech-savy individiuals who wish to use Whisper transcription technology. Notably, the application operates entirely offline, eleminating the need for any internet connection. This means that no data is send to the web. This offline-first approach provides a distinct advantage as sensitive data is not transmitted to external servers. The data exchange occurs directly between the server and the client.

To initiate the connection, the client simply enters the IP address of the server into a web browser. Subsequently, the client uploads an audio file to the server. The server promptly stores the file and initiates the processing of the audio to text conversion. Once the file has been successfully processed, it is immediately deleted from the server, enhancing data security. The text output, can be deleted by the user at their own will by clicking the remove button in the web interface. 

The underlying technology facilitating this functionality is a combination of [faster_whisper](https://github.com/SYSTRAN/faster-whisper) and [Flask](https://flask.palletsprojects.com/en/3.0.x/). Flask serves as the web framework for the Python programming language, providing a robust foundation for building web applications. Faster_whisper, on the other hand, is an optimized implementation of OpenAI's Whisper, delivering superior performance on CPU based inference.

Deployment of the program is made possible by [Docker](https://www.docker.com/) and [gunicorn](https://gunicorn.org/). Gunicorn serves the Flask web application. Gunicorn boosts the performance of the application significantly, as to accommodate a larger number of clients. Docker is used to deploy the program. Instructions for utilizing the program are outlined below.

The main user interface:
[Image](image/screenshot.png)

## Running the program from source code
```bash
docker compose up -d --no-deps --build simple_whisper_web --force-recreate      
```
And then use the following docker-compose.yml file:
```
version: '3'
services:
  simple_whisper_web:
    container_name: simple_whisper_web
    build: ./
    ports:
      - "9999:9999"
    environment:
      - GUNICORN_THREADS=2
      - USE_GPU=false
      - FLASK_DEBUG=false
```

## It is also possible to pull the image from Docker Hub:
```
version: '3'
services:
  simple_whisper_web:
    image: arnecuperus/simple_whisper_webapp:v1.0.4
    container_name: simple_whisper_web
    ports:
      - "9999:9999"
    environment:
      - GUNICORN_THREADS=2
      - USE_GPU=false
      - FLASK_DEBUG=false
      - MODEL_SIZE=large-v2
    volumes:
      - ./data:/data
    restart: unless-stopped
```

## Publishing the Docker image:

The program gets published by executing the following steps. 'v1.0.0' gets replaced with the correct version number.

## Build the Docker image:

```bash
docker build -t arnecuperus/simple_whisper_webapp:v1.0.0 .
```

## Tag the Docker image:

```bash
docker tag arnecuperus/simple_whisper_webapp:v1.0.0 arnecuperus/simple_whisper_webapp:v1.0.0
```

## Login to Docker Hub:

```bash
docker login
```

## Push the Docker image to Docker Hub:

```bash
docker push arnecuperus/simple_whisper_webapp:v1.0.0
```
