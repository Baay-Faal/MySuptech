from flask import Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'cle_secrete'
from app import routes