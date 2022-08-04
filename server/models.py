from db import db


class Doc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fileName = db.Column(db.Text, nullable=False)
    bucketName = db.Column(db.Text, nullable=True)
    mimeType = db.Column(db.Text, nullable=True)
    jobId = db.Column(db.Text, nullable=True)
    jobStatus = db.Column(db.Text, nullable=True)
    jobResponse = db.Column(db.JSON, nullable=True)
    documentMetadata = db.Column(db.JSON, nullable=True)
    blocks = db.Column(db.JSON, nullable=True)
    detectDocumentTextModelVersion = db.Column(db.Text, nullable=True)
    responseMetadata = db.Column(db.JSON, nullable=True)