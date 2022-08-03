from db import db


class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # img = db.Column(db.Text, unique=False, nullable=False)
    name = db.Column(db.Text, nullable=False)
    s3bucket = db.Column(db.Text, nullable=True)
    mimetype = db.Column(db.Text, nullable=True)
