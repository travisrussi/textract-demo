import os

from db import db_init, db
from models import Doc

from flask import Flask, request, Response, jsonify, redirect, json
from werkzeug.utils import secure_filename

# import asyncio
import boto3, botocore
from s3 import upload_file_to_s3
from textract import start_job, check_status, get_response

app= Flask(__name__)

heroku_url = os.environ.get('HEROKU_URL')

# Setup SQLAlchemy config
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI") # 'sqlite:///doc.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_init(app)

# Setup S3 integration
app.config['S3_BUCKET'] = os.environ.get("S3_BUCKET")
app.config['S3_KEY'] = os.environ.get("S3_KEY")
app.config['S3_SECRET'] = os.environ.get("S3_SECRET")
app.config['S3_LOCATION'] = 'http://{}.s3.amazonaws.com/'.format(app.config['S3_BUCKET'])

# Amazon S3 client
s3 = boto3.client(
   "s3",
   aws_access_key_id=app.config['S3_KEY'],
   aws_secret_access_key=app.config['S3_SECRET']
)

# Amazon Textract client
textract = boto3.client(
    'textract',
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

        doc = Doc(fileName=file.filename, mimeType=file.mimetype, bucketName=app.config["S3_BUCKET"])
        db.session.add(doc)
        db.session.commit()

        output = upload_file_to_s3(s3, file, app.config["S3_BUCKET"], app)

        return 'Doc Uploaded to S3!', 200
    else:
        return redirect("/")

@app.route('/document/<int:id>')
def get_doc_details(id):
    doc = Doc.query.filter_by(id=id).first()
    if not doc:
        return 'Doc Not Found!', 404

    return jsonify(
        file_name=doc.fileName,
        bucket_name=doc.bucketName,
        image_url=app.config["S3_LOCATION"] + doc.fileName
    )

@app.route('/document/all')
def get_all_doc_details():
    docs = Doc.query.all()

    return jsonify(docs)

@app.route('/document/<int:id>/download')
def get_doc_object(id):
    doc = Doc.query.filter_by(id=id).first()
    if not doc:
        return 'Doc Not Found!', 404

    return redirect(app.config["S3_LOCATION"] + doc.fileName)

@app.route('/document/<int:id>/parse/start')
def get_parse_start(id):

    doc = Doc.query.filter_by(id=id).first()
    if not doc:
        return 'Doc Not Found!', 404

    if not doc.jobStatus:
        jobId = start_job(textract, doc.bucketName, doc.fileName)

        if not jobId:
            return 'Unable to start job', 400

        doc.jobId = jobId
        doc.jobStatus = 'SUBMITTED'
        db.session.commit()

    return jsonify(
        id=doc.id,
        job_id=doc.jobId,
        job_status=doc.jobStatus
    )

@app.route('/document/<int:id>/parse/status')
def get_parse_status(id):

    doc = Doc.query.filter_by(id=id).first()
    if not doc:
        return 'Doc Not Found!', 404

    if not doc.jobId:
        return 'Doc Not Started!', 400

    if "DOWNLOADED" not in doc.jobStatus:

        jobStatus = check_status(textract, doc.jobId)
        
        if not jobStatus:
            return 'Unable to get job status', 400

        doc.jobStatus = jobStatus
        db.session.commit()

    return jsonify(
        id=doc.id,
        job_id=doc.jobId,
        job_status=doc.jobStatus
    )

@app.route('/document/<int:id>/parse/result')
def get_parse_result(id):

    doc = Doc.query.filter_by(id=id).first()
    if not doc:
        return 'Doc Not Found!', 404

    if not doc.jobId:
        return 'Doc Not Started!', 400

    # only download and parse the response onced
    if "DOWNLOADED" not in doc.jobStatus:
        response = get_response(textract, doc.jobId)

        if not response:
            return 'Unable to get job response', 400

        doc.jobResponse = json.dumps(response)

        if "JobStatus" in response:
            doc.jobStatus = response["JobStatus"]
        
        if "DocumentMetadata" in response:
            doc.documentMetadata = json.dumps(response["DocumentMetadata"])
        
        if "Blocks" in response:
            doc.blocks = json.dumps(response["Blocks"])
        
        if "ResponseMetadata" in response:
            doc.responseMetadata = json.dumps(response["ResponseMetadata"])

        if "DetectDocumentTextModelVersion" in response:
            doc.detectDocumentTextModelVersion = response["DetectDocumentTextModelVersion"]
    

    # manually set the jobStatus to 'DOWNLOADED' if the processing is complete and the response has be parsed
    if "SUCCEEDED" in doc.jobStatus and len(doc.jobResponse) > 0:
        doc.jobStatus = "DOWNLOADED"

    db.session.commit()

    return jsonify(
        id=doc.id,
        job_id=doc.jobId,
        job_status=doc.jobStatus,
        # job_response=json.loads(doc.jobResponse) if doc.jobResponse else "",
        blocks=json.loads(doc.blocks) if doc.blocks else "",
        document_metadata=json.loads(doc.documentMetadata) if doc.documentMetadata else "",
        response_metadata=json.loads(doc.responseMetadata) if doc.responseMetadata else "",
        detect_document_text_model_version=json.loads(doc.detectDocumentTextModelVersion) if doc.detectDocumentTextModelVersion else 0
    )
        