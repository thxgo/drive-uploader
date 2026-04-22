import os
import mimetypes
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Google Drive authentication 

CREDENTIALS_PATH= "credentials.json"
TOKEN_PATH = "token.json"
OUTBOX_FOLDER_ID= "your_id_here"
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

# folder creating/checking

def get_daily_folder(service):
    folders = service.files().list(
        q=f"'{OUTBOX_FOLDER_ID}' in parents",
        fields="files(id, name)"
    ).execute()["files"]
    today = datetime.now().strftime("%d-%m-%y")  
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
    return working_folder

# create batch for each script run

def create_batch(service, working_folder):
    now = datetime.now().strftime("%H-%M")
    batch_id = service.files().create(
            body={
                "name": f"batch-{now}",
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [working_folder]
            },
            fields="id"
    ).execute()["id"]
    return batch_id

# get file path from user and upload to batch

def upload_file(service, batch_id):
    while True:
        file_path = input("file path (or 'done' to finish): ") # TODO: add input validation 
        if file_path == "done":
            break
        mime_type, _ = mimetypes.guess_type(file_path)
        file_name = os.path.basename(file_path) 
        media = MediaFileUpload(file_path, mimetype=mime_type)
        file_id = service.files().create(
                body={
                    "name": file_name,
                    "parents": [batch_id]
                },
                media_body=media,
                fields="id",
                supportsAllDrives=True
        ).execute()["id"]
        print(f"file {file_name} was sucessfuly uploaded in Google Drive! - https://drive.google.com/file/d/{file_id}/view")
        # set file visibility to public
        service.permissions().create(
            fileId=file_id,
            body={
                "role": "reader",
                "type": "anyone"
            }
        ).execute()

def main():
    service = authenticate()
    working_folder = get_daily_folder(service)    
    batch_id = create_batch(service, working_folder)
    upload_file(service, batch_id)	
if __name__ == "__main__":
    main()
