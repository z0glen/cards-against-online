from flask import Flask
from flask_bootstrap import Bootstrap
#from flask_cors import CORS
from flask_socketio import SocketIO
import os


app = Flask(__name__)

bootstrap = Bootstrap(app)
#cors = CORS(app, resources={r'/*': {'origins': '*'}})
socketIO = SocketIO(app, cors_allowed_origins='http://localhost:8080')

app.secret_key = os.environ.get('SECRET_KEY', 'dev')
app.password = os.environ.get('CARDS_PASSWORD', 'dev')

from app import routes
