from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
import os

def upload_to_drive(file_path, file_name):
    try:
        # Controleer of het bestand bestaat op file_path
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Bestand niet gevonden: {file_path}")
        
        # Laad de credentials uit token.json
        creds = Credentials.from_authorized_user_file("token.json", ['https://www.googleapis.com/auth/drive.file'])
        
        # Bouw de Drive-service op
        service = build('drive', 'v3', credentials=creds)
        
        # Zorg dat je dit aanpast naar jouw daadwerkelijke folder-ID in Google Drive
        folder_id = "1s7_8EehBQBtAjMRSJlSTcOgx-VmoaxUK"
        
        file_metadata = {
            'name': file_name,
            'parents': [folder_id]
        }
        media = MediaFileUpload(file_path, mimetype='application/pdf')
        
        # Probeer het bestand aan te maken en uploaden
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print("API response:", file)
        return file.get('id')
    
    except HttpError as http_error:
        print("HTTP error tijdens upload:", http_error)
        raise http_error
    
    except Exception as err:
        print("Algemene fout tijdens upload:", err)
        raise err
