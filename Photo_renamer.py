import os.path, os, sys, re, io, json, \
File_uploader, Checks, shutil, File_downloader
import PySimpleGUI as sg
from PIL import Image

icon = "file_dru_icon.ico"
if os.path.exists("Properties.json"):
    with open("Properties.json") as Properties:
        windowProperties = json.load(Properties)

    if windowProperties.get("Theme") is None:
        sg.theme()

    else:
        sg.theme(windowProperties["Theme"])

#===============================================================================

def main():
    #defines layout for first window of module, answers affect path of program
    menu_def = [
        ["File", ["Download", "File Mover", "File Renamer",
        "Folder Creator", "---", "Properties", ["Themes", "Image Size"], "Exit"]],
    ]

    layout = [
        [sg.Menu(menu_def)],
        [sg.Text("Are multiple folders needed for renaming?"),
        sg.Radio("Yes", group_id=1, k="-YES-"),
        sg.Radio("No", group_id=1, k="-NO-")],
        [sg.Text("Is multiple folder move mode needed?"),
        sg.Radio("Yes", group_id=2, k="-YES_1-"),
        sg.Radio("No", group_id=2, k="-NO_1-")],
        [sg.Button("OK")],
    ]

    window = sg.Window(" ", layout, icon=icon)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == "OK":
            if values["-YES-"] is False and values["-NO-"] is False:
                if values["-YES_1-"] is False and values["-NO_1-"] is False:
                    sg.Popup("Please make a choice for both selections",
                    title=" ", icon=icon)

                else:
                    sg.Popup("Please make a choice for each selection",
                    title=" ", icon=icon)

            else:
                #defines paths after radios are selected
                if values["-YES-"] is True:
                    window.close()
                    multiple_photo_folders(values["-YES_1-"])

                else:
                    if values["-YES_1-"] is True:
                        window.close()
                        multiple_photo_folders_mover()

                    else:
                        window.close()
                        photo_renamer()

        if event == "Download":
            window.close()
            File_downloader.main()

        if event == "File Mover":
            window.close()
            multiple_photo_folders_mover()

        if event == "Folder Creator":
            window.close()
            multiple_photo_folders(False)

        if event == "File Renamer":
            window.close()
            photo_renamer()

        if event == "Themes":
            File_downloader.properties()
            window.close()
            main()

        if event == "Image Size":
            File_downloader.imageSize()
#===============================================================================

def mass_renamer(folder, file_list):
#Function is for mass renaming multiple selected files and follows format:
#file_name (#).file_extension
    layout = [
        [sg.Text("Input name to be mass labeled:")],
        [sg.In(enable_events=True, k="-IN-"), sg.Button("OK")],
    ]
    window = sg.Window(" ", layout, icon=icon)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == "OK":
            if Checks.input_field_check(values["-IN-"]) is True:
                continue

            else:
                try:
                    #iterates through each file selected and adds file extension
                    #and (#).
                    for count, file in enumerate(file_list):
                        regex = r"(\.\w+)$"
                        file_extension = re.search(regex, file)
                        file_extension.groups()

                        #if file extension present
                        if values["-IN-"].endswith(file_extension[0]) is True:
                            filename = os.path.join(folder + "\\" + file)
                            values["-IN-"] = values["-IN-"].replace(file_extension[0], "")
                            new_file = values["-IN-"] + "(" + str(count) + ")" + file_extension[0]
                            new_filename = os.path.join(folder, new_file)
                            os.rename(filename, new_filename)
                            file_list_1 = os.listdir(folder)
                            new_fnames = filenames(folder, os.listdir(folder))

                        #if file extension not present
                        else:
                            filename = os.path.join(folder + "\\" + file)
                            new_file = values["-IN-"] + "(" + str(count) + ")" + file_extension[0]
                            new_filename = os.path.join(folder, new_file)
                            os.rename(filename, new_filename)
                            new_fnames = filenames(folder, os.listdir(folder))

                    window.close()
                    #below statement is for updating values in previous window
                    return new_fnames

                except:
                    #name in use, try again
                    if new_file in os.listdir(folder):
                        sg.popup("This name is already in use", title=" ", icon=icon)

#===============================================================================

def photo_renamer():
    if os.path.exists("Properties.json"):
        with open("Properties.json") as Properties:
            windowProperties = json.load(Properties)

        if windowProperties.get("Size") is None:
            SIZE = (400, 400)

        else:
            SIZE = windowProperties["Size"]
    else:
        SIZE = (400, 400)

    #empty file_list is made to prevent crashes encountered by pushing "OK" early.
    file_list = []
    menu_def = [
        ["File", ["Download", "File Mover",
        "Folder Creator", "---", "Properties", ["Themes", "Image Size"], "Exit"]],
    ]
    #This sets up what will be on the left side of the window
    photo_column = [
        [sg.Menu(menu_def)],
        [sg.Text("Select source folder for file(s)")],
        [sg.In(enable_events=True, readonly=True, k="-FOLDER-",
        disabled_readonly_background_color=sg.theme_input_background_color()),
        sg.FolderBrowse()],
        [sg.Text("Select file(s) to rename:")],
        [sg.Listbox(values=file_list, select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED,
        enable_events=True, size=(40,20), k="-FILE_LIST-")],
    ]

    #This sets up what will be on the right side of the window
    viewer_column = [
        [sg.Image(k="-IMAGE-")],
        [sg.Text("New file name:")],
        [sg.In(k="-INPUT-", do_not_clear=False), sg.Button("OK")],
        [sg.Button("Mass rename"), sg.Button("Delete"), sg.Button("Upload")],
        [sg.Button("Rotate \u2B6E"), sg.Button("Rotate \u2B6F")]
    ]

    #This sets up the window with a vertical line seperating the two sections
    layout = [
        [sg.Column(photo_column),
        sg.VSeperator(),
        sg.Column(viewer_column)]
    ]

    #This creates the new window, finalize makes it so that it doesn't throw
    #a warning when the window gets updated
    window = sg.Window(" ", layout, icon=icon)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            sys.exit()

        if event == "-FOLDER-":
            if values["-FOLDER-"] == "":
                continue

            else:
                fnames = filenames(values["-FOLDER-"], os.listdir(values["-FOLDER-"]))
                if fnames is None:
                    fnames = []

                window["-FILE_LIST-"].update(fnames)

        elif event == "-FILE_LIST-":
            #The following block of code converts the picture from its original
            #size to a viewable thumbnail, while storing it in memory
            #The original file is unmodified during this conversion
            try:
                filename = os.path.join(
                    values["-FOLDER-"], values["-FILE_LIST-"][0]
                )
                if filename.lower().endswith(".pdf"):
                    image = Image.open("No preview available.png")

                else:
                    image = Image.open(filename)
                image.thumbnail(SIZE)
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["-IMAGE-"].update(data=bio.getvalue())

            except:
                sg.popup("File list is empty", title=" ", icon=icon)

        if event == "OK":
            if Checks.input_field_check(values["-INPUT-"]) is True:
                continue

            else:
                #This sets up a check to verify the file name is not in use,
                #and the searches the input field to see if the file extension
                #was typed there. If it was, it only uses the input field, else
                #it adds the file_extension from the original file.
                try:
                    regex = r"(\.\w+)$"
                    file_extension = re.search(regex, values["-FILE_LIST-"][0])
                    file_extension.groups()

                    if values["-INPUT-"].endswith(file_extension[0]) is True:
                        new_filename = os.path.join(values["-FOLDER-"],
                        values["-INPUT-"])
                        os.rename(filename, new_filename)
                        fnames = filenames(values["-FOLDER-"],
                        os.listdir(values["-FOLDER-"]))

                    else:
                        new_filename = os.path.join(values["-FOLDER-"],
                        values["-INPUT-"] + file_extension[0])
                        os.rename(filename, new_filename)
                        fnames = filenames(values["-FOLDER-"],
                        os.listdir(values["-FOLDER-"]))
                    window["-FILE_LIST-"].update(fnames)

                except:
                    #exception block to verify unique names and to select a
                    #photo to begin renaming.
                    if values["-FOLDER-"] == "":
                        sg.popup("Please select a folder for files to be renamed",
                        title=" ", icon=icon)

                    elif values["-INPUT-"] in file_list or values["-INPUT-"] \
                    + file_extension[0] in file_list:
                        sg.popup("This name is already in use",
                        title=" ", icon=icon)

                    else:
                        sg.popup("Please select a file from the left",
                         title=" ", icon=icon)

        if event == "Mass rename":
            if values["-FILE_LIST-"] == []:
                sg.popup("Please select files for mass rename first",
                title=" ", icon=icon)

            else:
                window["-FILE_LIST-"].update(mass_renamer(values["-FOLDER-"],
                values["-FILE_LIST-"]))

        #button event for deletion
        if event == "Delete":
            window["-FILE_LIST-"].update(delete(values["-FOLDER-"],
            values["-FILE_LIST-"]))
            window["-IMAGE-"].update()

        #button event for uploading; popups are for
        if event == "Upload":
            if values["-FOLDER-"] == "":
                sg.popup("Select a folder first", title=" ", icon=icon)

            elif values["-FILE_LIST-"] == []:
                sg.popup("Select a file first", title=" ", icon=icon)

            else:
                #work in progress to stop the program from exiting unexpectedly
                try:
                    creds = Checks.Cred_check()
                    if creds is None:
                        continue

                    #if credential check passed, move on to upload module
                    else:
                        File_uploader.Photo_uploader(values["-FOLDER-"],
                        os.listdir(values["-FOLDER-"]), creds, \
                        values["-FILE_LIST-"][0])

                #check to make sure there is a file to be uploaded selected
                except:
                    sg.Popup("Please select a file before uploading",
                    title=" ", icon=icon)

        #button event for when the clockwise button is pushed
        if event == "Rotate \u2B6E":
            if values["-FOLDER-"] == "":
                sg.popup("Select a folder first", title=" ", icon=icon)

            elif values["-FILE_LIST-"] == []:
                sg.popup("Select a file first", title=" ", icon=icon)

            elif filename.lower().endswith((".png", ".jpg", ".jpeg")):
                Image.open(filename).rotate(angle=270, expand=True).save(filename)
                imageRotate = Image.open(filename)
                imageRotate.thumbnail(SIZE)
                bio = io.BytesIO()
                imageRotate.save(bio, format="PNG")
                window["-IMAGE-"].update(data=bio.getvalue())

        #button event for when the counterclockwise button is pushed
        if event == "Rotate \u2B6F":
            if values["-FOLDER-"] == "":
                sg.popup("Select a folder first", title=" ", icon=icon)

            elif values["-FILE_LIST-"] == []:
                sg.popup("Select a file first", title=" ", icon=icon)

            elif filename.lower().endswith((".png", ".jpg", ".jpeg")):
                Image.open(filename).rotate(angle=90, expand=True).save(filename)
                imageRotate = Image.open(filename)
                imageRotate.thumbnail(SIZE)
                bio = io.BytesIO()
                imageRotate.save(bio, format="PNG")
                window["-IMAGE-"].update(data=bio.getvalue())

        #different options for the file menu
        if event == "Download":
            window.close()
            File_downloader.main()

        if event == "File Mover":
            window.close()
            multiple_photo_folders_mover()

        if event == "Folder Creator":
            window.close()
            multiple_photo_folders(False)

        if event == "Themes":
            File_downloader.properties()
            window.close()
            photo_renamer()

        if event == "Image Size":
            File_downloader.imageSize()
            window.close()
            photo_renamer()

#===============================================================================

def multiple_photo_folders_mover():
    if os.path.exists("Properties.json"):
        with open("Properties.json") as Properties:
            windowProperties = json.load(Properties)

        if windowProperties.get("Size") is None:
            SIZE = (400, 400)

        else:
            SIZE = windowProperties["Size"]
    else:
        SIZE = (400, 400)

    #empty file_lists is made to prevent crashes encountered by pushing "OK" early.
    file_list_1 = []
    file_list = []
    fnames = []
    menu_def = [
        ["File", ["Download", "File Renamer",
        "Folder Creator", "---", "Properties", ["Themes", "Image Size"], "Exit"]],
    ]
    #defines left side of window
    column_1 = [
        [sg.Text("Select source folder")],
        [sg.In(enable_events=True, readonly=True, k="-FOLDER-",
        disabled_readonly_background_color=sg.theme_input_background_color()),
        sg.FolderBrowse()],
        [sg.Text("Select file(s) to move:")],
        [sg.Listbox(values=file_list, select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED,
        enable_events=True, size=(40,20),k="-FILE_LIST-")],
    ]
    #defines middle of window
    column_2 = [
        [sg.Text("Photo preview")],
        [sg.Image(k="-IMAGE-")],
        [sg.Button("Move \u2192")],
    ]
    #defines right side of window
    column_3 = [
        [sg.Text("Select destination folder")],
        [sg.In(enable_events=True, readonly=True, k="-FOLDER_1-",
        disabled_readonly_background_color=sg.theme_input_background_color()),
        sg.FolderBrowse()],
        [sg.Listbox(values=file_list_1, select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED,
        enable_events=True, size=(40,20), k="-FILE_LIST_1-")],
        [sg.Button("Done")],
    ]
    #puts all 3 parts together with seperators
    layout = [
        [sg.Menu(menu_def)],
        [sg.Column(column_1),
        sg.VSeperator(),
        sg.Column(column_2),
        sg.VSeperator(),
        sg.Column(column_3)]
    ]
    window = sg.Window(" ", layout, icon=icon)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        #code block for left folder selection files
        if event == "-FOLDER-":
            if values["-FOLDER-"] == "":
                continue

            else:
                fnames = filenames(values["-FOLDER-"],
                os.listdir(values["-FOLDER-"]))
                window["-FILE_LIST-"].update(fnames)

        if event == "-FILE_LIST-":
            #The following block of code converts the picture from its original
            #size to a viewable thumbnail, while storing it in memory
            #The original file is unmodified during this conversion.
            #If file is .pdf, displays placeholder image.
            try:
                filename = os.path.join(values["-FOLDER-"],
                values["-FILE_LIST-"][0])

                if filename.lower().endswith(".pdf"):
                    image = Image.open("No preview available.png")

                else:
                    image = Image.open(filename)

                image.thumbnail(SIZE)
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["-IMAGE-"].update(data=bio.getvalue())

            except:
                sg.popup("Left file list is empty", title=" ", icon=icon)

        #code block for right folder selection files
        if event == "-FOLDER_1-":
            if values["-FOLDER_1-"] == "":
                continue

            else:
                fnames_1 = filenames(values["-FOLDER_1-"],
                os.listdir(values["-FOLDER_1-"]))

                #if listdir creates an empty file list, this changes the type from None to list
                if fnames_1 is None:
                    fnames_1 = []

                window["-FILE_LIST_1-"].update(fnames_1)

        if event == "-FILE_LIST_1-":
            #The following block of code converts the picture from its original
            #size to a viewable thumbnail, while storing it in memory
            #The original file is unmodified during this conversion
            #If file is .pdf, displays placeholder image.
            try:
                filename = os.path.join(values["-FOLDER_1-"],
                values["-FILE_LIST_1-"][0])

                if filename.lower().endswith(".pdf"):
                    image = Image.open("No preview available.png")

                else:
                    image = Image.open(filename)

                image.thumbnail(SIZE)
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["-IMAGE-"].update(data=bio.getvalue())

            except:
                sg.popup("Right file list is empty", title=" ", icon=icon)

        #moves file from left folder to right folder
        if event == "Move \u2192":
            #checks to make sure both folder fields are selected first
            if values["-FOLDER-"] == "" or values["-FOLDER_1-"] == "":
                sg.popup("Please select a folder before moving files!",
                title=" ", icon=icon)
            #checks to see if folders are the same in case a mistke was made selecting them
            elif values["-FOLDER-"] == values["-FOLDER_1-"]:
                continue

            #shutil.move is needed to move between different lettered drives
            else:
                for file in values["-FILE_LIST-"]:
                    shutil.move(os.path.join(values["-FOLDER-"], file),
                    os.path.join(values["-FOLDER_1-"], file))
                    fnames.remove(file)

                    #if listdir creates an empty file list, this changes the type from None to list
                    if fnames_1 is None:
                        fnames_1 = []
                    fnames_1.append(file)

                window["-FILE_LIST-"].update(fnames)
                window["-FILE_LIST_1-"].update(fnames_1)
                window["-IMAGE-"].update()

        #Button event for done moves onto file renamer function
        if event == "Done":
            window.close()
            photo_renamer()

        #different options for the file menu
        if event == "Download":
            window.close()
            File_downloader.main()

        if event == "Folder Creator":
            window.close()
            multiple_photo_folders(False)

        if event == "File Renamer":
            window.close()
            photo_renamer()

        if event == "Themes":
            File_downloader.properties()
            window.close()
            multiple_photo_folders_mover()

        if event == "Image Size":
            File_downloader.imageSize()
            window.close()
            multiple_photo_folders_mover()

#===============================================================================

def multiple_photo_folders(YES_1_check_value):
    #define layout for folder creation Window
    menu_def = [
        ["File", ["Download", "File Renamer",
        "Folder Mover", "---", "Properties", ["Themes", "Image Size"], "Exit"]],
    ]

    layout = [
        [sg.Menu(menu_def)],
        [sg.Text("Where are folders going to be created?"),
        sg.In("", readonly=True, k="-FOLDER-",
        disabled_readonly_background_color=sg.theme_input_background_color()),
        sg.FolderBrowse()],
        [sg.Text("How many folders need to be created?"),
        sg.In("", k="-IN-")],
        [sg.Button("OK")],
    ]

    window = sg.Window(" ", layout, icon=icon)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        #first 2 cases as defined, only accept # and folder.
        if event == "OK":
            if values["-IN-"].strip().isdigit() is not True:
                sg.popup("Please enter a number", title=" ", icon=icon)

            elif values["-FOLDER-"] == "":
                sg.popup("Please select a folder before continuing",
                title=" ", icon=icon)

            else:
                #checks path and proceeds to correct function if folders needed is 0.
                window.close()
                if int(values["-IN-"]) == 0 and YES_1_check_value is True:
                    multiple_photo_folders_mover()

                elif int(values["-IN-"]) == 0 and YES_1_check_value is False:
                    photo_renamer()

                else:
                    #for loop iterates to max value input in folders desired field
                    for folder_num in range(int(values["-IN-"])):
                        layout_1 = [
                            [sg.Text("Folder {} name:".format(folder_num + 1)),
                            sg.Input("", k="-IN_1-")],
                            [sg.Button("OK")],
                        ]

                        #enable_close_attempted_event is added to break apart WIN_CLOSED
                        #event referenced by window.close() and an exit when 'x' is clicked
                        window_1 = sg.Window(" ", layout_1,
                        enable_close_attempted_event=True, icon=icon)
                        #creates each folder in a separate window, one at a time
                        while True:
                            event_1, values_1 = window_1.read()

                            #break event to ensure loop still continues
                            if event_1 == "Exit" or event_1 == sg.WIN_CLOSED:
                                break

                            #sys.exit() is to immediately close program instead of window only
                            if event_1 == sg.WINDOW_CLOSE_ATTEMPTED_EVENT:
                                sys.exit()

                            if event_1 == "OK":
                                if Checks.input_field_check(values_1["-IN_1-"]) is True:
                                    continue

                                else:
                                    #checks file list to make sure folder
                                    #name isn't already in use.
                                    file_list = os.listdir(values["-FOLDER-"])
                                    for i, file in enumerate(file_list):
                                        file_list[i] = file_list[i].lower()

                                    if values_1["-IN_1-"].lower() in file_list:
                                        sg.popup("Name already in use, choose another",
                                        title=" ", icon=icon)

                                    else:
                                        window_1.close()
                                        os.mkdir(values["-FOLDER-"] + "/" + values_1["-IN_1-"])

                    #checks original path and continues program based on that
                    if YES_1_check_value is True:
                        multiple_photo_folders_mover()

                    else:
                        photo_renamer()

        #different options for the file menu
        if event == "Download":
            window.close()
            File_downloader.main()

        if event == "Folder Mover":
            window.close()
            multiple_photo_folders_mover()

        if event == "File Renamer":
            window.close()
            photo_renamer()

        if event == "Themes":
            File_downloader.properties()
            window.close()
            multiple_photo_folders(YES_1_check_value)

        if event == "Image Size":
            File_downloader.imageSize()

#===============================================================================

def filenames(folder, file_list):
    list_filenames= [
        f
        for f in file_list
        if os.path.isfile(os.path.join(folder,f))
        and f.lower().endswith((".png", ".jpg", ".jpeg", ".pdf"))
    ]

    return list_filenames

#===============================================================================

def delete(folder, fileList):
    if folder == "":
        sg.popup("Select a folder first", title=" ", icon=icon)

    elif fileList == []:
        sg.popup("Select a file first", title=" ", icon=icon)

    else:
        #This initiates a new window that asks for confirmation before deletion
        layoutDelete = [
            [sg.Text("This will permanently delete the file. Continue?")],
            [sg.Button("Yes"), sg.Button("No")]
        ]

        windowDelete = sg.Window(" ", layoutDelete, icon=icon)
        while True:
            eventDelete, valuesDelete = windowDelete.read()
            if eventDelete == "Exit" or eventDelete == sg.WIN_CLOSED:
                break

            #Yes button push deletes the file and then updates file list
            #and window to no longer show deleted file
            if eventDelete == "Yes":
                windowDelete.close()

                for file in fileList:
                    os.remove(os.path.join(folder, file))

                fnamesDelete = filenames(folder,
                os.listdir(folder))

                if fnamesDelete is None:
                    fnamesDelete = []

                return fnamesDelete

            else:
                windowDelete.close()
