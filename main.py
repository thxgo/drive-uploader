from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime

# Google Drive authentication 

CREDENTIALS_PATH= "credentials.json"
OUTBOX_FOLDER_ID= "your_id_here"
SCOPES = ["https://www.googleapis.com/auth/drive"]

creds = service_account.Credentials.from_service_account_file(
    CREDENTIALS_PATH,
    scopes=SCOPES
)
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
