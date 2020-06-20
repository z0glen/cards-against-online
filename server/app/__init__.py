from flask import Flask
from flask_socketio import SocketIO
import os


app = Flask(__name__)

socketIO = SocketIO(app, cors_allowed_origins="*")

app.secret_key = os.environ.get('SECRET_KEY', 'dev')
app.password = os.environ.get('CARDS_PASSWORD', 'dev')

from app import routes
