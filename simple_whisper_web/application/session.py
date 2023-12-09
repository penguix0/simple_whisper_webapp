from application import app, User, db
from flask import request, redirect, url_for, session
from uuid import uuid4

@app.route('/set_user_id')
def set_user_id():
    ## Check if not already has an user_id
    user_id = session.get('user_id')
    if user_id:
        return redirect(url_for('upload'))

    # Generate unique user_id
    user_id = str(uuid4())

    # Set user_id in the session
    user = User(id=user_id)
    session['user_id'] = user_id

    with app.app_context():
        db.session.add(user)
        db.session.commit()

    return redirect(url_for('upload'))


@app.route('/clear_user_id')
def clear_user_id():
    # Retrieve user from the database using the user_id from the session
    user_id = session.pop('user_id', None)

    if user_id:
        user = User.query.filter_by(id=user_id).first()

        # Remove user from the database
        if user:
            with app.app_context():
                db.session.delete(user)
                db.session.commit()

    return redirect(url_for('upload'))
