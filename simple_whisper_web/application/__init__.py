from flask import Flask
from os import path, remove, makedirs
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import logging

log_format = '[%(asctime)s] [%(levelname)s] %(message)s'
date_format = '%d/%b/%Y %H:%M:%S'

# Set up the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# Configure the root logger with the right format
logging.basicConfig(format=log_format, datefmt=date_format, level=logging.DEBUG)
logging.getLogger("faster_whisper").setLevel(logging.DEBUG)

basedir = path.abspath(path.dirname(__file__))
parent_dir = path.abspath(path.join(basedir, ".."))
logger.debug(f"Parent directory: {parent_dir}")

## Create an app object
app = Flask(__name__)
## Create config
app.config.from_pyfile(path.join(parent_dir, 'config.py'))

logger.info(f'Created Flask app, debug is set to {app.config["DEBUG"]}')

## Init database
if not path.exists(app.config["DATABASE_FOLDER"]):
    logger.info("Database folder does not exist, creating it now")
    makedirs(app.config["DATABASE_FOLDER"])

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + path.join(app.config["DATABASE_FOLDER"], app.config["DATABASE_FILENAME"])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

logger.info(f'Creating database object from file at {app.config["SQLALCHEMY_DATABASE_URI"]}.')
db = SQLAlchemy(app)

from uuid import uuid4
from datetime import datetime, timedelta

class User(db.Model):
    id = db.Column(db.String, primary_key=True, default=str(uuid4()), nullable=False)
    audio_files = db.relationship('AudioFile', backref='user', lazy=True)

class AudioFile(db.Model):
    id = db.Column(db.String, primary_key=True, default=str(uuid4()))
    file_name = db.Column(db.String, nullable=True, default="file")
    path = db.Column(db.String, nullable=False)
    result = db.Column(db.String, nullable=True)
    length = db.Column(db.Integer, nullable=False, default=0)
    progress = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now)
    expiry_date = db.Column(db.DateTime, default=(datetime.now()+timedelta(days=app.config["EXPIRE_TIME"])))

    user_id = db.Column(db.String, db.ForeignKey('user.id'), nullable=False)

    def get_expiry_date_as_str(self):
        format_string = '%Y-%m-%d %H:%M:%S'
        return self.expiry_date.strftime(format_string)


logger.info("Resetting and creating database")
app.app_context().push()
db.create_all()
db.session.query(AudioFile).delete()
db.session.commit()

logger.info(f'Audio files will get deleted in {app.config["EXPIRE_TIME"]} day(s) from creation.')

from .helper import remove_files_in_relative_directory

if not path.exists(app.config["UPLOAD_FOLDER"]):
    logger.info("Upload folder does not exist, creating it now")
    makedirs(app.config["UPLOAD_FOLDER"])
else:
    logger.info("Cleaning files from previous boot:")
    remove_files_in_relative_directory(app.config["UPLOAD_FOLDER"])


import threading
from .whisper.que_worker import audio_transcription_worker 
from .whisper.init_model import init_model
from .database.expire_data_worker import data_expiry_worker
from .helper import is_thread_running

thread_name = "audio_transcription_thread"
if not path.exists(app.config["MODEL_PATH"]):
    logger.info("Model folder does not exist, creating it now")
    makedirs(app.config["MODEL_PATH"])

# Check if the thread is already running
if not is_thread_running(thread_name):
    logger.info("Spawning transcription thread")
    model = init_model(app.config["MODEL_PATH"], app.config["USE_GPU"], app.config["MODEL_SIZE"])
    audio_transcription_thread = threading.Thread(target=audio_transcription_worker, args=(model,), name=thread_name)
    audio_transcription_thread.start()
    logger.debug("Transcription thread started")
else:
    logger.info(f"Thread {thread_name} is already running.")

thread_name = "data_expiry_thread"
# Check if the thread is already running
if not is_thread_running(thread_name):
    logger.info("Spawning data expiry thread")
    expiry_thread = threading.Thread(target=data_expiry_worker, args=(), name=thread_name)
    expiry_thread.start()
    logger.debug("Data expiry thread started")
else:
    logger.info(f"Thread {thread_name} is already running.")

## Import views
logger.debug("Importing views")
from .views.upload import upload
logger.debug("Upload imported")
from .views.index import index
logger.debug("Index imported")
from .session import set_user_id, clear_user_id
logger.debug("Session imported")
from .queue import get_queue_length, get_file_queue_state
logger.debug("Queue imported")