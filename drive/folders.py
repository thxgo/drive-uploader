from datetime import datetime

OUTBOX_FOLDER_ID= "your_folder_id_here"

# folder creating/checking
def get_daily_folder(service):
    try:
    	folders = service.files().list(
            q=f"'{OUTBOX_FOLDER_ID}' in parents",
            fields="files(id, name)"
        ).execute()["files"]
    except Exception as e:
        print("OUTBOX_FOLDER_ID invalid. If you haven't configured it yet, see README.md")
        return None
    today = datetime.now().strftime("%d-%m-%y")
    found = False
    working_folder = None
    for folder in folders:
        if folder["name"] == today:
            found = True
            working_folder = folder["id"]
            print(f"found existing folder: {today} - https://drive.google.com/drive/u/2/folders/{working_folder}")
    if not found:
        working_folder = service.files().create(
            body={
                "name": today,
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [OUTBOX_FOLDER_ID]
            },
            fields="id"
        ).execute()["id"]
        print(f"created folder: {today} - https://drive.google.com/drive/u/2/folders/{working_folder}")
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
