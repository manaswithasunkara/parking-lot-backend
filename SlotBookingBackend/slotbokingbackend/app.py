from flask import Flask
from flask_cors import CORS
import datetime

app = Flask(__name__)
app.secret_key = "secret key"
app.config['PERMANENT_SESSION_LIFETIME'] =  datetime.timedelta(minutes=10)
CORS(app)
