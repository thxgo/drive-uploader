import os
import mimetypes
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Google Drive authentication 

CREDENTIALS_PATH= "credentials.json"
OUTBOX_FOLDER_ID= "your_id_here"
SCOPES = ["https://www.googleapis.com/auth/drive"]


if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
else:     
    flow = InstalledAppFlow.from_client_secrets_file(
        CREDENTIALS_PATH,
        scopes=SCOPES
        )
    creds = flow.run_local_server(port=0)
    with open("token.json", "w") as token:
        token.write(creds.to_json())       
service = build("drive", "v3", credentials=creds)

# list folders inside outbox

folders = service.files().list(
    q=f"'{OUTBOX_FOLDER_ID}' in parents",
    fields="files(id, name)"
).execute()["files"]

# folder creating/checking

today = datetime.now().strftime("%d-%m-%y")  
# now = datetime.now().isoformat() # DON'T DELETE, can be used for logs later

found = False
working_folder = None

for folder in folders:
    if folder["name"] == today:
        found = True
        working_folder = folder["id"] 
        print(f"folder {today} exists! - https://drive.google.com/drive/u/2/folders/{working_folder}")
if not found:
    working_folder = service.files().create(
        body={
            "name": today,
            "mimeType": "application/vnd.google-apps.folder",
            "parents": [OUTBOX_FOLDER_ID]
        },
        fields="id"
        ).execute()["id"]
    print(f"folder {today} created! - https://drive.google.com/drive/u/2/folders/{working_folder}")

# get file path from user and upload to working folder

file_path = input("file path: ") # TODO: add input validation 
mime_type, _ = mimetypes.guess_type(file_path)
file_name = os.path.basename(file_path) 
media = MediaFileUpload(file_path, mimetype=mime_type)

file_id = service.files().create(
        body={
            "name": file_name,
            "parents": [working_folder]
        },
        media_body=media,
        fields="id",
        supportsAllDrives=True
).execute()["id"]
print(f"file {file_name} was sucessfuly uploaded in Google Drive! - https://drive.google.com/file/d/{file_id}/view")
