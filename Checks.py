import json, os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import PySimpleGUI as sg

if os.path.exists("Theme.json"):
    with open("Theme.json", "r") as Theme:
        windowTheme = json.load(Theme)
    sg.theme(windowTheme)

def input_field_check(input_field):
    """Helper function to perform input field checks against all spaces and illegal characters"""
    #This checks to make sure that the input is not blank or spaces
    if input_field.isspace() == True or input_field == "":
        sg.popup("The file field cannot be empty", title = " ")
        return True

    #This checks for invalid file characters
    if input_field.find("<") != -1 or input_field.find(">") != -1 \
        or input_field.find(":") != -1 or input_field.find("\\") != -1 \
        or input_field.find("/") != -1 or input_field.find("\"") != -1 \
        or input_field.find("|") != -1 or input_field.find("?") != -1 \
        or input_field.find("*") != -1:
            sg.popup("The following characters cannot be used:"
                "< > : \ / \" | ? * ", title= " ")
            return True

    else:
        return False

#===============================================================================

#This code block is from the Google Python Quickstart for Google Drive API,
#with a try/except block added in. Try/except block was added to make sure that
#when the token.json file expires, user is notified and file is deleted.
#This makes it so that user doesn't have to start from the beginning.
def Cred_check():
    try:
        creds = None
        SCOPES = ["https://www.googleapis.com/auth/drive", \
        "https://www.googleapis.com/auth/photoslibrary"]

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

        return creds

    except:
        sg.popup("Deleting token.json. Try again.", title= " ")
        os.remove("token.json")

#===============================================================================
