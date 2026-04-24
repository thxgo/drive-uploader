import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Google Drive authentication 
CREDENTIALS_PATH= "credentials.json"
TOKEN_PATH = "token.json"
SCOPES = ["https://www.googleapis.com/auth/drive"]

def authenticate():
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_PATH,
            scopes=SCOPES
            )
        creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
    service = build("drive", "v3", credentials=creds)
    return service                       
