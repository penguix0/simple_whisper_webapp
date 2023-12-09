from time import sleep
from os import path, remove
from .process_audio import process_audio
from application import app, AudioFile, db, logger

def audio_transcription_worker(model):
    transcribing = False
    que_length = 0

    with app.app_context(): 
        while True:
            que_length = AudioFile.query.filter_by(result=None).count()
            
            if not transcribing and not que_length == 0: 
                transcribing = True
                for file in AudioFile.query.order_by(AudioFile.created_at).all():
                    if file.result == None:
                        logger.debug(f"Starting to process {file.path}")
                        file.result = process_audio(model, file)
                        db.session.commit()

                        transcribing = False

                        if path.exists(file.path):
                            remove(file.path)

                        break
            sleep(1)