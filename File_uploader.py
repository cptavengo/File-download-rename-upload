import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import PySimpleGUI as sg
import Input_field_check

def photo_uploader(folder, file_list):
    try:
        creds = None
        SCOPES = "https://www.googleapis.com/auth/drive.file"

        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)

            with open("token.json", "w") as token:
                token.write(creds.to_json())

    except:
        sg.popup("Try deleting token.json and try again.")

    DRIVE = build("drive", "v3", credentials=creds)

    layout = [
        [sg.Text("Enter Drive folder name:")],
        [sg.In(enable_events=True, k="-IN-"), sg.Button("OK")],
    ]
    window = sg.Window(" ", layout)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == "OK":
            if Input_field_check.input_field_check(values["-IN-"]) == True:
                pass

            else:
                try:
                    window.close()
                    #Folder creation block
                    file_metadata = {
                        "name": values["-IN-"],
                        "mimeType": "application/vnd.google-apps.folder"
                    }
                    DRIVE_FOLDER = DRIVE.files().create(body=file_metadata, fields="id").execute()
                    layout_1 = [
                        [sg.Text("Uploading files now...")],
                        [sg.ProgressBar(len(file_list), orientation="h", size=(20,20), k="-PROG-")],
                    ]
                    window_1 = sg.Window(" ", layout_1)
                    i = 1

                    #File upload block
                    for files in file_list:
                        if os.path.isfile(os.path.join(folder, files)) \
                        and files.lower().endswith((".png", ".jpg", ".jpeg", ".pdf")):
                            event_1, values_1 = window_1.read(timeout=10)
                            metadata = {
                                "name": files,
                                "parents": [DRIVE_FOLDER.get("id")]
                            }
                            file_path = folder + "/" + files
                            file = DRIVE.files().create(body=metadata, fields="id",
                            media_body=file_path, media_mime_type="Image/jpeg").execute()
                            window_1["-PROG-"].update(i+1)
                            i += 1
                    window_1.close()
                except:
                    sg.popup("Something didn't work.")

if __name__ == "__main__":
    photo_uploader()
