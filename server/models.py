from dataclasses import dataclass
from db import db

# dataclass attribute allows for JSON serialization of the object
# https://stackoverflow.com/a/57732785


@dataclass
class Doc(db.Model):
    id: int
    fileName: str
    bucketName: str
    mimeType: str
    jobId: str
    jobStatus: str
    jobResponse: str
    documentMetadata: str
    blocks: str
    detectDocumentTextModelVersion: str
    responseMetadata: str

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