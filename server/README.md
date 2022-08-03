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
