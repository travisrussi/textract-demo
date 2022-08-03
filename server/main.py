import os

from db import db_init, db
from models import Img

from flask import Flask

app= Flask(__name__)

# Setup SQLAlchemy config
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI") # 'sqlite:///img.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)

@app.route('/')
def index():
  return "<h1>Welcome to CodingX</h1><h2>PROJECT_PATH: " + os.environ.get('PROJECT_PATH') + "</h2>"