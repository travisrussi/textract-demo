import os

from db import db_init, db
from models import Img

from flask import Flask, request, Response, jsonify
from werkzeug.utils import secure_filename


app= Flask(__name__)

heroku_url = os.environ.get('HEROKU_URL')

# Setup SQLAlchemy config
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI") # 'sqlite:///img.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)

@app.route('/')
def index():
  return "<h1>Welcome to CodingX</h1><h2>PROJECT_PATH: " + os.environ.get('PROJECT_PATH') + "</h2>"


@app.route("/upload", methods=["POST"])
def upload_file():
    if "pic" not in request.files:
        return "No pic key in request.files"
    file = request.files["pic"]
    if file.filename == "":
        return "Please select a file"
    if file:
        file.filename = secure_filename(file.filename)
        #     mimetype = file.mimetype

        if not file.filename or not file.mimetype:
            return 'Bad upload!', 400

        img = Img(img=file.read(), name=file.filename, mimetype=file.mimetype)
        # img = Img(name=file.filename, mimetype=file.mimetype)
        db.session.add(img)
        db.session.commit()

        return 'Img Uploaded!', 200
    else:
        return redirect("/")


@app.route('/image/<int:id>')
def get_img_object(id):
    img = Img.query.filter_by(id=id).first()
    if not img:
        return 'Img Not Found!', 404

    return Response(img.img, mimetype=img.mimetype)

@app.route('/<int:id>')
def get_img_details(id):
    img = Img.query.filter_by(id=id).first()
    if not img:
        return 'Img Not Found!', 404

    return jsonify(
        filename=img.name,
        image_url=heroku_url + "image/" + str(img.id)
    )