from time import sleep
from os import path, remove
from application import app, AudioFile, db, logger
from datetime import date, timedelta, datetime

def data_expiry_worker():
    with app.app_context(): 
        while True:
            for file in AudioFile.query.order_by(AudioFile.created_at).all():
                current_date = datetime.now()

                if file.expiry_date <= current_date:
                    logger.debug(f"File {file.file_name} is expired and will be deleted")
                    if path.exists(file.path):
                        remove(file.path)
                        logger.debug(f"{file.path} was deleted succesfully from filesystem")
                    
                    db.session.delete(file)
                    db.session.commit()
                    logger.debug(f"{file.file_name} was deleted succesfully from database")

                
            sleep(1)