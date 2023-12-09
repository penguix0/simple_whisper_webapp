from application import app, AudioFile, db
from flask import jsonify, session, request

@app.route('/get_queue_length', methods=["GET"])
def get_queue_length():
    current_user_id = session.get('user_id')

    queue_length = len(AudioFile.query.filter_by(result=None).filter(AudioFile.user_id != current_user_id).all())    

    return jsonify({"queue_length": queue_length}), 200

@app.route('/get_file_queue_state', methods=["GET"])
def get_file_queue_state():
    current_user_id = session.get('user_id')

    file_id = request.args.get('file_id')

    false_response = {"is_being_processed": "false","finished":"false", "progress":"0/0"}
    processing_response = {"is_being_processed": "true","finished":"false", "progress":"0/0"}
    true_response = {"is_being_processed": "false","finished":"true", "progress":"0/0"}
    if not file_id:
        return jsonify(false_response), 200

    first_item_in_queue = AudioFile.query.filter_by(result=None).first()  
    
    if first_item_in_queue == None: 
        return jsonify(true_response), 200

    if first_item_in_queue.id == file_id and first_item_in_queue.result == None:
        processing_response["progress"] = f"{first_item_in_queue.progress}/{first_item_in_queue.length}"
        return jsonify(processing_response), 200
    elif first_item_in_queue.id == file_id and not first_item_in_queue.result == None:
        return jsonify(true_response), 200

    return false_response

