from application import app, AudioFile, User, db, logger
from flask import render_template, request, redirect, url_for, jsonify, session
from werkzeug.utils import secure_filename
import os
from uuid import uuid4
from pydub import AudioSegment
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, validators, HiddenField
import datetime

def get_audio_duration(file_path):
    try:
        audio = AudioSegment.from_file(file_path)
        duration_in_seconds = len(audio) / 1000  # Convert milliseconds to seconds
        return round(duration_in_seconds)
    except Exception as e:
        logger.warning(f"Error: {e}")
        return None

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]

class UploadForm(FlaskForm):
    file = FileField('File', validators=[FileRequired(), FileAllowed(app.config["ALLOWED_EXTENSIONS"], 'Alleen audio bestanden zijn toegestaan!')])

class SelectedFile:
    def __init__(self, name, length, file_id, result, expiry_date):
        self.name = name
        self.length = length
        self.id = file_id
        self.result = result
        self.expiry_date = expiry_date

@app.route('/upload', methods=["GET", "POST"])
def upload():
    current_user_id = session.get('user_id')

    if not current_user_id:
        return redirect(url_for('set_user_id'))

    file_form = UploadForm()

    if request.method == "POST" and file_form.validate_on_submit():
        file = file_form.file.data
        old_secure_filename = secure_filename(file.filename)

        id = str(uuid4())

        ## Save file with new filename
        new_path = os.path.join(app.config['UPLOAD_FOLDER'], id+os.path.splitext(old_secure_filename)[1])
        file.save(new_path)

        ## Create database entry
        audio_file = AudioFile(id=id, path=new_path, file_name=old_secure_filename, length=get_audio_duration(new_path), user_id=current_user_id)

        db.session.add(audio_file)
        db.session.commit()

    selected_file_id = request.args.get('selected_file')

    selected_file_query = AudioFile.query.filter_by(user_id=current_user_id, id=selected_file_id).first()

    selected_file = None
    if selected_file_query:
        selected_file = SelectedFile(selected_file_query.file_name, selected_file_query.length, selected_file_query.id, selected_file_query.result, selected_file_query.get_expiry_date_as_str())

    files = AudioFile.query.filter_by(user_id=current_user_id).all()

    expire_time = app.config["EXPIRE_TIME"]

    return render_template('upload.html', files=files, file_form=file_form, selected_file=selected_file)


@app.route('/remove_audio_file', methods=["GET"])
def remove_audio_file():
    if request.method == "GET":
        current_user_id = session.get('user_id')

        if not current_user_id:
            return redirect(url_for('set_user_id'))

        file_id = request.args.get("file_id")

        if file_id: 
            audio_file = AudioFile.query.filter_by(id=file_id,user_id=current_user_id).first()

            # Remove user from the database
            if audio_file:
                if os.path.exists(audio_file.path):
                    os.remove(audio_file.path)

                db.session.delete(audio_file)
                db.session.commit()

                return jsonify({"status": "success"}), 200

    return jsonify({"status": "failed"}), 406