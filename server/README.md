# Textract Demo Server

Simple Python API using Flask and SqlAlchemy to process documents via AWS Textract service.

## Building the Project 

To setup the server to run locally:
```bash
    cd server
    pip3 install -r requirements.txt
```

To run the server locally (via Heroku CLI):
```bash
    cd server
    heroku local
```

## API Routes

- `POST /document` - Upload a document for processing
- `GET  /document/all` - Returns all the documents in the database
- `GET  /document/[id]` - Returns the details of a single document
- `GET  /document/[id]/download` - Redirects to the original document in S3
- `GET  /document/[id]/parse/start` - Initiates the textract parsing process
- `GET  /document/[id]/parse/status` - Gets the current status of the textract parsing process
- `GET  /document/[id]/parse/result` - Gets the result of the textract parsing process

### Add Dependencies

After adding some dependencies, update the `requirements.txt` file:
```bash
pip3 freeze > requirements.txt
```bash

## Setup For Deployment to Heroku

- [Heroku CLI Cheatsheet](https://gist.github.com/1000miles/4547e07d7815b9701c145c3a3860ffb9)
- [How to Deply a Flask App on Heroku](https://dev.to/techparida/how-to-deploy-a-flask-app-on-heroku-heb)
- [Subdir-Heroku-Buildpack Docs](https://github.com/timanovsky/subdir-heroku-buildpack)
- [Heroku-Config](https://github.com/xavdid/heroku-config)

Because this project just uses one Git repo for both client and server, you have to setup the heroku deployment from the `server` subfolder.

1. Add an environment variable `PROJECT_PATH` set to `server`
2. Add the subfolder build pack: `https://github.com/timanovsky/subdir-heroku-buildpack`

### Specify Default App for Heroku CLI
If you created the app from the Heroku web application and are using Github as the repo, then you have to set the app manually in the CLI (otherwise, it requires `--app [app-name]` for all CLI commands):

```bash
heroku git:remote -a app-name
```

### Environment Variables
We'll need to setup some environment variables.

First, set them up on Heroku via the CLI:
```bash
heroku config:add test1=bob
```

Then, pull them down locally:
```bash
heroku plugins:install heroku-config
heroku config:pull --overwrite
```

Note that any locally created environment variables in the `.ENV` file persist when pulling the config down from Heroku.  Using the `--overwrite` flag will overwrite existing variables.

To push the local `.env` variables up to Heroku:

```bash
heroku config:push --overwrite
```

It's also helpful to set the Heroku Url as a config variable for access in the app:
```bash
heroku config:set HEROKU_URL=$(heroku info -s | grep web_url | cut -d= -f2)
```

## Setup SqlAlchemy

(SqlAlchemy for Flask)[https://flask-sqlalchemy.palletsprojects.com/en/2.x/]

## Setup S3 Integration

To upload to an S3 bucket, you have to create a user via IAM with S3 permissions. Make sure the S3 bucket has `ACLs enabled` for `Object Ownership`. You also have to uncheck the two `Block public access` flags for `ACLs`.

Create these environment variables:
```bash
heroku config:set AWS_DEFAULT_REGION=us-east-1
heroku config:set S3_BUCKET=my-s3-upload-bucket
heroku config:set S3_KEY=iam-user-key
heroku config:set S3_SECRET=iam-user-secret
```

Once the IAM and S3 items are setup on AWS, doing the file upload via Flask is pretty straightforward using these instructions:

- [2 ways to upload files to Amazon S3 in Flask](https://rajrajhans.com/2020/06/2-ways-to-upload-files-to-s3-in-flask/)
