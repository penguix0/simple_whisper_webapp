## ONLY use for debug purposes

from application import app

app.run(host=app.config["HOST"], port=app.config["PORT"], debug=app.config["DEBUG"])