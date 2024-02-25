from os import path, mkdir, environ
## library to generate secret key
from secrets import token_urlsafe

## Secret key which gets automatically generated
SECRET_KEY = token_urlsafe(32)

HOST = "0.0.0.0"
PORT = 9999

DEBUG = environ.get('FLASK_DEBUG', '').lower() == 'true' if environ.get('FLASK_DEBUG', '').lower() else False

UPLOAD_FOLDER = "/data/uploads"
MODEL_PATH = "/data/models/"
DATABASE_FOLDER = "/data/database"
ALLOWED_EXTENSIONS = {'mp3', 'm4a'}
DATABASE_FILENAME = "database.db"
MODEL_SIZE = environ.get('MODEL_SIZE', 'medium')
USE_GPU = environ.get('USE_GPU', '').lower() == 'true' if environ.get('USE_GPU', '').lower() else False
EXPIRE_TIME = int(environ.get('EXPIRE_TIME')) if environ.get('EXPIRE_TIME') else 10 # Days