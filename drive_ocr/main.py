
import io
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

class Drive_OCR:
    def __init__(self,filename) -> None:
        self.filename = filename
        self.SCOPES = ['https://www.googleapis.com/auth/drive']
        self.credentials = "./credentials.json"
        self.pickle = "token.pickle"

    def main(self) -> str:
        creds = None
        if os.path.exists(self.pickle):
            with open(self.pickle, 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials, self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(self.pickle, 'wb') as token:
                pickle.dump(creds, token)

        service = build('drive', 'v3', credentials=creds)

        # For Uploading Image into Drive
        mime = 'application/vnd.google-apps.document'
        file_metadata = {'name': self.filename, 'mimeType': mime}
        file = service.files().create(
            body=file_metadata,
            media_body=MediaFileUpload(self.filename, mimetype=mime)
        ).execute()
        print('File ID: %s' % file.get('id'))

        # It will export drive image into Doc
        request = service.files().export_media(fileId=file.get('id'),mimeType="text/plain")

        # For Downloading Doc Image data by request
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))

        # It will delete file from drive base on ID
        service.files().delete(fileId=file.get('id')).execute()

        # It will print data into terminal
        output = fh.getvalue().decode()
        return output
    
def create_text_file(text, filename,page):
    print("image text extracted: "+str(page))

    with open(filename, "a", encoding="utf-8") as f:
        f.write(text)
        





if __name__ == '__main__':
    output_file = "my_file"

    current_directory = os.getcwd()
    i = 1
    for filename in os.listdir(current_directory+'/img'):
        img = f"page_{i}.jpg"
        print(img)
        try:
            ob = Drive_OCR(f"./img/{img}")
            text = ob.main()
            i+=1
        except:
            print(f'faild--{img}')
            i+=1
            continue

        create_text_file(text, output_file,i)
        