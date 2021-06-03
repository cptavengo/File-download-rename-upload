import os.path, json, Input_field_check, sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import PySimpleGUI as sg

#===============================================================================
#This code block is from the Google Python Quickstart for Google Drive API,
#with a try/except block added in. Try/except block was added to make sure that
#when the token.json file expires, user is notified and file is deleted.
#This makes it so that user doesn't have to start from the beginning.
def Cred_check(folder, file_list):
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

        Photo_uploader(folder, file_list, creds)

    except:
        sg.popup("Deleting token.json. Try 'OK' again.")
        os.remove("token.json")

#===============================================================================

def Photo_uploader(folder, file_list, creds):
    #gathers necessary information to upload files into Drive
    DRIVE = build("drive", "v3", credentials=creds)

    layout = [
        [sg.Text("Single file upload?"), sg.Radio("Yes", group_id=1, k="-YES-"),
        sg.Radio("No", group_id=1, k="-NO-")],
        [sg.Text("Share files?"), sg.Radio("Yes", group_id=2, k="-YES_1-"),
        sg.Radio("No", group_id=2, k= "-NO_1-")],
        [sg.Button("OK")]
    ]

    window = sg.Window(" ", layout)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == "OK":
            try:
                window.close()
                #Folder creation block
                if values["-YES-"] == True:
                    if values["-YES_1-"] == True:

                        for files in file_list:
                            if os.path.isfile(os.path.join(folder, files)) \
                            and files.lower().endswith((".png", ".jpg", ".jpeg", ".pdf")):
                                #File upload block
                                metadata = {
                                    "name": files,
                                }
                                file_path = folder + "/" + files
                                file = DRIVE.files().create(body=metadata, fields="id", \
                                media_body=file_path, media_mime_type="Image/jpeg").execute()
                                #opens a separate .json file that contains shared folder information.
                                with open("Permissions.json", "r") as read_file:
                                    user_permissions = json.load(read_file)
                                #execute permissions on the uploaded folder
                                DRIVE.permissions().create(body=user_permissions, \
                                sendNotificationEmail=False, fileId=file.get("id")).execute()
                        sg.popup("File uploaded!")

                    else:
                        for files in file_list:
                            if os.path.isfile(os.path.join(folder, files)) \
                            and files.lower().endswith((".png", ".jpg", ".jpeg", ".pdf")):
                                #File upload block
                                metadata = {
                                    "name": files,
                                }
                                file_path = folder + "/" + files
                                file = DRIVE.files().create(body=metadata, fields="id", \
                                media_body=file_path, media_mime_type="Image/jpeg").execute()
                        sg.popup("File uploaded!")

                else:
                    layout_1 = [
                        [sg.Text("Enter Drive folder name:")],
                        [sg.In(enable_events=True, k="-IN-"), sg.Button("OK")]
                    ]

                    window_1 = sg.Window(" ", layout_1)

                    while True:
                        event_1, values_1 = window_1.read()
                        if event_1 == "Exit" or event_1 == sg.WIN_CLOSED:
                            break

                        if event_1 == "OK":
                            if Input_field_check.input_field_check(values_1["-IN-"]) == True:
                                pass
                            window_1.close()

                            if values["-YES_1-"] == True:
                                file_metadata = {
                                    "name": values_1["-IN-"],
                                    "mimeType": "application/vnd.google-apps.folder"
                                }
                                DRIVE_FOLDER = DRIVE.files().create(body=file_metadata, \
                                fields="id").execute()
                                #opens a separate .json file that contains shared folder information.
                                with open("Permissions.json", "r") as read_file:
                                    user_permissions = json.load(read_file)
                                #execute permissions on the uploaded folder
                                DRIVE.permissions().create(body=user_permissions, \
                                sendNotificationEmail=False, fileId=DRIVE_FOLDER.get("id")).execute()
                                #create a separate file list for progress bar
                                file_list_1 = []

                                for files in file_list:
                                    if os.path.isfile(os.path.join(folder, files)) \
                                    and files.lower().endswith((".png", ".jpg", ".jpeg", ".pdf")):
                                        file_list_1.append(files)
                                #opens new window for progress bar
                                layout_2 = [
                                    [sg.Text("Uploading files now...")],
                                    [sg.ProgressBar(len(file_list_1), orientation="h", \
                                    size=(20,20), k="-PROG-")],
                                    [sg.Text(k="-TEXT-", size=(20,0))]
                                ]
                                window_2 = sg.Window(" ", layout_2)
                                #File upload block
                                i = 1
                                #iterate through each file and upload them to the selected folder
                                for files in file_list:
                                    if os.path.isfile(os.path.join(folder, files)) \
                                    and files.lower().endswith((".png", ".jpg", ".jpeg", ".pdf")):
                                        event_2, values_2 = window_2.read(timeout=10)
                                        metadata = {
                                            "name": files,
                                            "parents": [DRIVE_FOLDER.get("id")]
                                        }
                                        file_path = folder + "/" + files
                                        file = DRIVE.files().create(body=metadata, fields="id",
                                        media_body=file_path, media_mime_type="Image/jpeg").execute()
                                        #below code updates progress bar and file counter during upload
                                        window_2["-PROG-"].update(i)
                                        window_2["-TEXT-"].update("{} / {} files uploaded" \
                                        .format(str(i), str(len(file_list_1))))
                                        i += 1

                                    if event_2 == "Exit" or event_2 == sg.WIN_CLOSED:
                                        break
                                window_2.close()

                            else:
                                file_metadata = {
                                    "name": values_1["-IN-"],
                                    "mimeType": "application/vnd.google-apps.folder"
                                }
                                DRIVE_FOLDER = DRIVE.files().create(body=file_metadata, \
                                fields="id").execute()
                                #create a separate file list for progress bar
                                file_list_1 = []
                                for files in file_list:
                                    if os.path.isfile(os.path.join(folder, files)) \
                                    and files.lower().endswith((".png", ".jpg", ".jpeg", ".pdf")):
                                        file_list_1.append(files)
                                #opens new window for progress bar
                                layout_2 = [
                                    [sg.Text("Uploading files now...")],
                                    [sg.ProgressBar(len(file_list_1), orientation="h", \
                                    size=(20,20), k="-PROG-")],
                                    [sg.Text(k="-TEXT-", size=(20,0))]
                                ]
                                window_2 = sg.Window(" ", layout_2)
                                #File upload block
                                i = 1
                                #iterate through each file and upload them to the selected folder
                                for files in file_list:
                                    if os.path.isfile(os.path.join(folder, files)) \
                                    and files.lower().endswith((".png", ".jpg", ".jpeg", ".pdf")):
                                        event_2, values_2 = window_2.read(timeout=10)
                                        metadata = {
                                            "name": files,
                                            "parents": [DRIVE_FOLDER.get("id")]
                                        }
                                        file_path = folder + "/" + files
                                        file = DRIVE.files().create(body=metadata, fields="id",
                                        media_body=file_path, media_mime_type="Image/jpeg").execute()
                                        #below code updates progress bar and file counter during upload
                                        window_2["-PROG-"].update(i)
                                        window_2["-TEXT-"].update("{} / {} files uploaded" \
                                        .format(str(i), str(len(file_list_1))))
                                        i += 1

                                    if event_2 == "Exit" or event_2 == sg.WIN_CLOSED:
                                        break
                                window_2.close()

            except:
                sg.popup("Something didn't work.")
