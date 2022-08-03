import os

from db import db_init, db
from models import Img

from flask import Flask, request, Response, jsonify, redirect
from werkzeug.utils import secure_filename

# import asyncio
import boto3, botocore
from s3 import upload_file_to_s3

app= Flask(__name__)

heroku_url = os.environ.get('HEROKU_URL')

# Setup SQLAlchemy config
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI") # 'sqlite:///img.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)

# Setup S3 integration
app.config['S3_BUCKET'] = os.environ.get("S3_BUCKET")
app.config['S3_KEY'] = os.environ.get("S3_KEY")
app.config['S3_SECRET'] = os.environ.get("S3_SECRET")
app.config['S3_LOCATION'] = 'http://{}.s3.amazonaws.com/'.format(app.config['S3_BUCKET'])

s3 = boto3.client(
   "s3",
   aws_access_key_id=app.config['S3_KEY'],
   aws_secret_access_key=app.config['S3_SECRET']
)

@app.route('/')
def index():
  return "<h1>Textract Demo Server</h1><h2>PROJECT_PATH: " + os.environ.get('PROJECT_PATH') + "</h2>"


@app.route("/upload", methods=["POST"])
def upload_file():
    if "doc" not in request.files:
        return "No doc key in request.files"
    file = request.files["doc"]
    if file.filename == "":
        return "Please select a file"
    if file:
        file.filename = secure_filename(file.filename)
        #     mimetype = file.mimetype

        if not file.filename or not file.mimetype:
            return 'Bad upload!', 400

        img = Img(name=file.filename, mimetype=file.mimetype, s3bucket=app.config["S3_BUCKET"])
        # img = Img(name=file.filename, mimetype=file.mimetype)
        db.session.add(img)
        db.session.commit()

        output = upload_file_to_s3(s3, file, app.config["S3_BUCKET"], app)

        return 'Img Uploaded to S3!', 200
    else:
        return redirect("/")


@app.route('/image/<int:id>')
def get_img_object(id):
    img = Img.query.filter_by(id=id).first()
    if not img:
        return 'Img Not Found!', 404

    return redirect(app.config["S3_LOCATION"] + img.name)

@app.route('/<int:id>')
def get_img_details(id):
    img = Img.query.filter_by(id=id).first()
    if not img:
        return 'Img Not Found!', 404

    return jsonify(
        filename=img.name,
        image_url=app.config["S3_LOCATION"] + img.name
    )

