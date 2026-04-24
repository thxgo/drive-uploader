import os
import mimetypes
from googleapiclient.http import MediaFileUpload

# get file from user and upload to batch
def upload_file(service, batch_id, files):
    for file_path in files:
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
        print(f"file {file_name} was sucessfuly uploaded to Google Drive! - https://drive.google.com/file/d/{file_id}/view")
        # set file visibility to public
        service.permissions().create(
            fileId=file_id,
            body={
                "role": "reader",
                "type": "anyone"
            }
        ).execute()
