from flask import Flask
from flask_bootstrap import Bootstrap
from flask_cors import CORS
import os

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY', 'dev')
app.password = os.environ.get('CARDS_PASSWORD', 'dev')

bootstrap = Bootstrap(app)
cors = CORS(app, resources={r'/*': {'origins': '*'}})

from app import routes
