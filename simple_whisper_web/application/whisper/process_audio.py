from faster_whisper import WhisperModel
from application import app, db, AudioFile, logger
from pydub import AudioSegment

def get_audio_duration(file_path):
    try:
        audio = AudioSegment.from_file(file_path)
        duration_in_seconds = len(audio) / 1000  # Convert milliseconds to seconds
        return duration_in_seconds
    except Exception as e:
        logger.warning(f"Error: {e}")
        return None


def process_audio(model, file):
    segments, _ = model.transcribe(file.path)
    duration = get_audio_duration(file.path)

    ## Format text
    total_text = ""
    for segment in segments:
        total_text += (segment.text + "\n")

        ## Update progress
        with app.app_context(): 
            audio_file = AudioFile.query.get(file.id)
            if audio_file:
                audio_file.progress = round(segment.end)
                db.session.commit()


    return total_text