from os import environ
# Gunicorn config variables
loglevel = "debug"
errorlog = "-"  # stderr
accesslog = "-"  # stdout
worker_tmp_dir = "/dev/shm"
graceful_timeout = 600
timeout = 600
keepalive = 5
threads = int(environ.get("GUNICORN_THREADS", "1")) if environ.get("GUNICORN_THREADS", "").isdigit() else 1