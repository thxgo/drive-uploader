import os
import mimetypes
from googleapiclient.http import MediaFileUpload

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
