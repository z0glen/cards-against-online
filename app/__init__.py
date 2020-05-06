from flask import Flask
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY', 'dev')
app.password = os.environ.get('CARDS_PASSWORD', 'dev')

bootstrap = Bootstrap(app)

from app import routes
