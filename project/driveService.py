from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

SERVICE_ACCOUNT_FILE = 'credentials.json'
SCOPES = ['https://www.googleapis.com/auth/drive']
FOLDER_ID = os.getenv("DRIVE_FOLDER_ID")


class DriveService:

    def __init__(self):
        #authentication
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES
        )
        self.drive_service = build('drive', 'v3', credentials=creds)

    def upload_image_to_folder(self, image_path, customName):
        file_metadata = {
            'name': customName,
            'parents': [FOLDER_ID]
        }
        media = MediaFileUpload(image_path, mimetype='image/jpeg')
        file = self.drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, webViewLink'
        ).execute()
        print(f"Uploaded: {file['webViewLink']}")

        return file['webViewLink']

