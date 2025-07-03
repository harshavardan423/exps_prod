from flask import Flask,session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
import os

app = Flask(__name__, static_folder='static')
app.wsgi_app = ProxyFix(app.wsgi_app)
app.secret_key = 'your-secret-key-here'  # Change this to a secure value

# Configure CORS with specific origins
CORS(app, origins=[
    "http://exclusive.agentsofatom.com:1002",
    "https://exclusive.agentsofatom.com:1002",
    # Add other domains as needed
    "http://localhost:3000",  # if you need local development
    "http://127.0.0.1:3000"
])

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '..', 'exposed_instances.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

def create_tables():
    with app.app_context():
        db.create_all()

from app import routes