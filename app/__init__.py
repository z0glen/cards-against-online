from flask import Flask
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_socketio import SocketIO
import os


app = Flask(__name__)

socketIO = SocketIO(app)
bootstrap = Bootstrap(app)
cors = CORS(app, resources={r'/*': {'origins': '*'}})

app.secret_key = os.environ.get('SECRET_KEY', 'dev')
app.password = os.environ.get('CARDS_PASSWORD', 'dev')

from app import routes
