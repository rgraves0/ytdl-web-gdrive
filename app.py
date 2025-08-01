from flask import Flask, request, render_template, redirect, url_for, Response
from functools import wraps
import os
import json
from youtube_dl import YoutubeDL
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
GDRIVE_FOLDER_ID = os.getenv("GDRIVE_FOLDER_ID")

# Load credentials from env
creds_json = os.getenv("GOOGLE_CREDENTIALS_B64")
creds_dict = json.loads(creds_json)
credentials = service_account.Credentials.from_service_account_info(creds_dict, scopes=["https://www.googleapis.com/auth/drive"])
drive_service = build('drive', 'v3', credentials=credentials)

# Basic Auth
def check_auth(username, password):
    return username == USERNAME and password == PASSWORD

def authenticate():
    return Response('Could not verify your access level for that URL.\n'
                    'You have to login with proper credentials', 401,
                    {'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/', methods=['GET', 'POST'])
@requires_auth
def index():
    message = ""
    if request.method == 'POST':
        url = request.form['url']
        ydl_opts = {
            'format': 'best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
        }
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        file_metadata = {
            'name': os.path.basename(filename),
            'parents': [GDRIVE_FOLDER_ID]
        }
        media = MediaFileUpload(filename, resumable=True)
        drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        message = f"Uploaded: {os.path.basename(filename)} to Google Drive"

    return render_template('index.html', message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
