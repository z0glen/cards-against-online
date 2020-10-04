from flask import Flask
from flask_socketio import SocketIO
import os
import logging
import sys


app = Flask(__name__)

app.logger = logging.getLogger(__name__)
app.logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)

socketIO = SocketIO(app, cors_allowed_origins="*")

app.secret_key = os.environ.get('SECRET_KEY', 'dev')
app.password = os.environ.get('CARDS_PASSWORD', 'dev')

from app import routes
