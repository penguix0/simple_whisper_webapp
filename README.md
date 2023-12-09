## Run the image
```bash
docker compose up -d --no-deps --build simple_whisper_web --force-recreate      
```
With the following docker-compose.yml file:
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

## Instead you can also pull the image:
```
version: '3'
services:
  simple_whisper_web:
    image: arnecuperus/simple_whisper_webapp:latest
    container_name: simple_whisper_web
    ports:
      - "9999:9999"
    environment:
      - GUNICORN_THREADS=2
      - USE_GPU=false
      - FLASK_DEBUG=false
```

Here are the steps to publish the image:

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


```bash
docker pull arnecuperus/simple_whisper_webapp:v1.0.0
```