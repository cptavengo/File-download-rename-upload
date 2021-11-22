import os.path, json, Checks, sys, re, File_downloader
from googleapiclient.discovery import build
import PySimpleGUI as sg

icon = "file_dru_icon.ico"
if os.path.exists("Properties.json"):
    with open("Properties.json") as Properties:
        windowProperties = json.load(Properties)

    if windowProperties.get("Theme") is None:
        sg.theme()

    else:
        sg.theme(windowProperties["Theme"])

#===============================================================================

def file_sharing(built_drive, FILE_LIST_VALUES, upload_files, \
single_file_upload, yes_no_2_value):
    nextPageToken = "empty"
    file_name_id_list = []
    #Cuts down on folder loading time by reading from an existing file
    if os.path.exists("Drive Folder List.json") and yes_no_2_value is True:
        with open("Drive Folder List.json", "r") as read_file:
            file_name_id_list = json.load(read_file)
        file_name_list = [i["name"] for i in file_name_id_list if "name" in i]
        file_name_list.sort()

    #Reads from the user's Google Drive folders to find everything, will take a while
    else:
        while nextPageToken != "":
            if nextPageToken == "empty":
                nextPageToken = ""

            else:
                nextPageToken

            Drive_list = built_drive.files().list(pageToken=nextPageToken,\
            fields="nextPageToken, files(mimeType, name, id)").execute()

            for file in Drive_list.get("files"):
                if file["mimeType"] == "application/vnd.google-apps.folder":
                    file_name_id_list.append({"name": file["name"], "id": file["id"]})
            nextPageToken = Drive_list.get("nextPageToken", "")

            for i in file_name_id_list:
                file_name_list = [i["name"] for i in file_name_id_list if "name" in i]
                file_name_list.sort()

            #Creates file to help reduce load time of folders in the future
            with open("Drive Folder List.json", "w") as Folder_list:
                json.dump(file_name_id_list, Folder_list, indent=1)

    layout_shared_folder_select = [
        [sg.Text("Select shared folder to upload to")],
        [sg.Listbox(values=file_name_list, enable_events=True, size =(40,20),
        k="-FOLDER LIST-")],
        [sg.Button("OK")]
    ]

    window_shared_folder_select = sg.Window(" ", layout_shared_folder_select,
    icon=icon)

    while True:
        event_shared, values_shared = window_shared_folder_select.read()
        if event_shared == sg.WIN_CLOSED or event_shared == "Exit":
            break

        if event_shared == "-FOLDER LIST-":
            name = next((item for item in file_name_id_list if item["name"] == \
            values_shared["-FOLDER LIST-"][0]), None)
            parent_ID = name["id"]

        if event_shared == "OK":
            try:
                if single_file_upload is True:
                    for files in upload_files:
                        if os.path.isfile(os.path.join(FILE_LIST_VALUES, files)) \
                        and files.lower().endswith((".png", ".jpg", ".jpeg")):
                            #File upload block
                            metadata = {
                                "name": files,
                                "parents": [parent_ID]
                            }
                            file_path = FILE_LIST_VALUES + "/" + files
                            file = built_drive.files().create(body=metadata, fields="id", \
                            media_body=file_path, media_mime_type="Image/jpeg").execute()

                        elif os.path.isfile(os.path.join(FILE_LIST_VALUES, files)) \
                        and files.lower().endswith((".pdf")):
                            #File upload block
                            metadata = {
                                "name": files,
                                "parents": [parent_ID]
                            }
                            file_path = FILE_LIST_VALUES + "/" + files
                            file = built_drive.files().create(body=metadata,
                            fields="id",media_body=file_path,
                            media_mime_type="application/pdf").execute()

                    sg.popup("File uploaded to {}".format(values_shared["-FOLDER LIST-"][0]),
                    title=" ", icon=icon)
                    window_shared_folder_select.close()

                else:
                    regex = r"(\w+.+/)"
                    folder_search = re.search(regex, FILE_LIST_VALUES)
                    folder_search.groups()
                    folder_name = FILE_LIST_VALUES.replace(folder_search[0], "")
                    file_metadata = {
                        "name": folder_name,
                        "mimeType": "application/vnd.google-apps.folder",
                        "parents": [parent_ID]
                    }
                    DRIVE_FOLDER = built_drive.files().create(body=file_metadata,
                    fields="id").execute()
                    #create a separate file list for progress bar
                    file_list_1 = []

                    for files in upload_files:
                        if os.path.isfile(os.path.join(FILE_LIST_VALUES, files)) \
                        and files.lower().endswith((".png", ".jpg", ".jpeg", ".pdf")):
                            file_list_1.append(files)

                    #opens new window for progress bar
                    layout_2 = [
                        [sg.Text("Uploading files now...")],
                        [sg.ProgressBar(len(file_list_1), orientation="h",
                        size=(20,20), k="-PROG-")],
                        [sg.Text(k="-TEXT-", size=(20,0))]
                    ]

                    window_2 = sg.Window(" ", layout_2, icon=icon)
                    #iterate through each file and upload them to the selected folder
                    for i, files in enumerate(upload_files, 1):
                        event_2, values_2 = window_2.read(timeout=10)

                        if os.path.isfile(os.path.join(FILE_LIST_VALUES, files)) \
                        and files.lower().endswith((".png", ".jpg", ".jpeg")):
                            metadata = {
                                "name": files,
                                "parents": [DRIVE_FOLDER.get("id")]
                            }
                            file_path = FILE_LIST_VALUES + "/" + files
                            file = built_drive.files().create(body=metadata,
                            fields="id", media_body=file_path,
                            media_mime_type="Image/jpeg").execute()

                            #below code updates progress bar and file counter during upload
                            window_2["-PROG-"].update(i)
                            window_2["-TEXT-"].update("{} / {} files uploaded" \
                            .format(str(i), str(len(file_list_1))))

                        elif os.path.isfile(os.path.join(FILE_LIST_VALUES, files)) \
                        and files.lower().endswith(".pdf"):
                            metadata = {
                                "name": files,
                                "parents": [DRIVE_FOLDER.get("id")]
                            }
                            file_path = FILE_LIST_VALUES + "/" + files
                            file = built_drive.files().create(body=metadata, fields="id",
                            media_body=file_path, media_mime_type="application/pdf").execute()
                            #below code updates progress bar and file counter during upload
                            window_2["-PROG-"].update(i)
                            window_2["-TEXT-"].update("{} / {} files uploaded" \
                            .format(str(i), str(len(file_list_1))))

                        if event_2 == "Exit" or event_2 == sg.WIN_CLOSED:
                            break
                    window_2.close()
                    sg.popup("Folder and files uploaded to {}".format(
                    values_shared["-FOLDER LIST-"][0]), title=" ", icon=icon)
                window_shared_folder_select.close()

            except:
                sg.Popup("Please select a folder to upload to.", title=" ", icon=icon)

#===============================================================================

def Photo_uploader(folder, file_list, creds, single_file_value):
    #gathers necessary information to upload files into Drive
    DRIVE = build("drive", "v3", credentials=creds)

    section1 = [
        [sg.Text("**WARNING: This list may be out of date!**")]
    ]

    section2 = [
        [sg.Text("Will take a while for large Drives to update!")]
    ]

    layout = [
        [sg.Text("Single file upload (Folder uploaded too on 'No' selection)?"),
        sg.Radio("Yes", group_id=1, k="-YES-"),
        sg.Radio("No", group_id=1, k="-NO-")],
        [sg.Text("Share files?"), sg.Radio("Yes", group_id=2, k="-YES_1-"),
        sg.Radio("No", group_id=2, k="-NO_1-")],
        [sg.Text("Use existing Drive folder list?"),
        sg.Radio("Yes", group_id=3, enable_events=True, k="-YES_2-"),
        sg.Radio("No", group_id=3, enable_events=True, k="-NO_2-")],
        [File_downloader.collapse(section1, "-Sec1-")],
        [File_downloader.collapse(section2, "-Sec2-")],
        [sg.Button("OK")]
    ]

    window = sg.Window(" ", layout, icon=icon)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == "-YES_2-":
            opened1, opened2 = True, False
            window["-Sec1-"].update(visible=opened1)
            window["-Sec2-"].update(visible=opened2)

        if event == "-NO_2-":
            opened1, opened2 = False, True
            window["-Sec1-"].update(visible=opened1)
            window["-Sec2-"].update(visible=opened2)

        if event == "OK":
            if values["-YES-"] == values["-NO-"] \
            or values["-YES_1-"] == values["-NO_1-"] \
            or values["-YES_2-"] == values["-NO_2-"]:
                sg.Popup("Please make a choice for each selection", title=" ",
                icon=icon)

            else:
                try:
                    window.close()
                    #Folder creation block
                    file_upload_list = []
                    file_upload_list.append(single_file_value)
                    if values["-YES-"] is True:

                        if values["-YES_1-"] is True:
                            file_sharing(DRIVE, folder, file_upload_list,
                            values["-YES-"], values["-YES_2-"])

                        else:
                            if os.path.isfile(os.path.join(folder,
                            single_file_value)) and single_file_value.lower() \
                            .endswith((".png", ".jpg", ".jpeg")):
                                #File upload block
                                metadata = {
                                    "name": single_file_value,
                                }
                                file_path = folder + "/" + single_file_value
                                file = DRIVE.files().create(body=metadata,
                                fields="id", media_body=file_path,
                                media_mime_type="Image/jpeg").execute()

                            if os.path.isfile(os.path.join(folder, single_file_value)) \
                            and single_file_value.lower().endswith((".pdf")):
                                #File upload block
                                metadata = {
                                    "name": single_file_value,
                                }
                                file_path = folder + "/" + single_file_value
                                file = DRIVE.files().create(body=metadata, fields="id", \
                                media_body=file_path, media_mime_type="application/pdf").execute()
                            sg.popup("File uploaded!", title=" ", icon=icon)

                    else:
                        if values["-YES_1-"] is True:
                            file_sharing(DRIVE, folder, file_list, values["-YES-"], values["-YES_2-"])

                        else:
                            regex = r"(\w+.+/)"
                            folder_search = re.search(regex, folder)
                            folder_search.groups()
                            folder_name = folder.replace(folder_search[0], "")
                            file_metadata = {
                                "name": folder_name,
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
                            #iterate through each file and upload them to the selected folder
                            for i, files in enumerate(file_list):
                                event_2, values_2 = window_2.read()
                                if os.path.isfile(os.path.join(folder, files)) \
                                and files.lower().endswith((".png", ".jpg", ".jpeg")):
                                    metadata = {
                                        "name": files,
                                        "parents": [DRIVE_FOLDER.get("id")]
                                    }
                                    file_path = folder + "/" + files
                                    file = DRIVE.files().create(body=metadata,
                                    fields="id", media_body=file_path,
                                    media_mime_type="Image/jpeg").execute()
                                    #code updates progress bar and file counter during upload
                                    window_2["-PROG-"].update(i)
                                    window_2["-TEXT-"].update("{} / {} files uploaded" \
                                    .format(str(i), str(len(file_list_1))))

                                if os.path.isfile(os.path.join(folder, files)) \
                                and files.lower().endswith((".pdf")):
                                    metadata = {
                                        "name": files,
                                        "parents": [DRIVE_FOLDER.get("id")]
                                    }
                                    file_path = folder + "/" + files
                                    file = DRIVE.files().create(body=metadata,
                                    fields="id", media_body=file_path,
                                    media_mime_type="application/pdf").execute()
                                    #below code updates progress bar and file counter during upload
                                    window_2["-PROG-"].update(i)
                                    window_2["-TEXT-"].update("{} / {} files uploaded" \
                                    .format(str(i), str(len(file_list_1))))

                                if event_2 == "Exit" or event_2 == sg.WIN_CLOSED:
                                    break
                            window_2.close()

                except :
                    sg.popup("Something didn't work.", title=" ", icon=icon)
