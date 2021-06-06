import os.path, os, sys, re, io, File_uploader, Input_field_check
import PySimpleGUI as sg
from PIL import Image

#===============================================================================

def main():
    #defines layout for first window of module, questions affect path of program
    layout = [
        [sg.Text("Are multiple folders needed for renaming?"),
        sg.Radio("Yes", group_id=1, k="-YES-"), sg.Radio("No", group_id=1)],
        [sg.Text("Is multiple folder move mode needed?"),
        sg.Radio("Yes", group_id=2, k="-YES_1-"), sg.Radio("No", group_id=2)],
        [sg.Button("OK")],
    ]

    window = sg.Window(" ", layout)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == "OK":
            #defines paths after radios are selected
            if values["-YES-"] == True: #Y and Y or N path
                window.close()
                multiple_photo_folders(values["-YES_1-"])

            else:
                if values["-YES_1-"] == True: #NY path
                    window.close()
                    multiple_photo_folders_mover()

                else: #NN path
                    window.close()
                    photo_renamer()

        else:
            if values["-YES-"] == True: #Y and Y or N path
                window.close()
                multiple_photo_folders(values["-YES_1-"])
            else:
                if values["-YES_1-"] == True: #NY path
                    window.close()
                    multiple_photo_folders_mover()

                else: #NN path
                    window.close()
                    photo_renamer()

#===============================================================================

def mass_renamer(folder, file_list):
#Function is for mass renaming multiple selected files and follows format:
#file_name (#).file_extension
    layout = [
        [sg.Text("Input name to be mass labeled:")],
        [sg.In(enable_events=True, key="-IN-"), sg.Button("OK")],
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
                    #iterates through each file selected and adds file extension
                    #and (#).
                    count = 1
                    for file in file_list:
                        regex = r"(\.\w+)$"
                        file_extension = re.search(regex, file)
                        file_extension.groups()
                        #if file extension present
                        if values["-IN-"].endswith(file_extension[0]) == True:
                            filename = os.path.join(folder + "\\" + file)
                            values["-IN-"] = values["-IN-"].replace(file_extension[0], "")
                            new_file = values["-IN-"] + "(" + str(count) + ")" + file_extension[0]
                            new_filename = os.path.join(folder, new_file)
                            os.rename(filename, new_filename)
                            file_list_1 = os.listdir(folder)
                            new_fnames = [
                                f
                                for f in file_list_1
                                if os.path.isfile(os.path.join(folder,f))
                                and f.lower().endswith((".png", ".jpg", ".jpeg", ".pdf"))
                            ]
                        #if file extension not present
                        else:
                            filename = os.path.join(folder + "\\" + file)
                            new_file = values["-IN-"] + "(" + str(count) + ")" + file_extension[0]
                            new_filename = os.path.join(folder, new_file)
                            os.rename(filename, new_filename)
                            file_list_1 = os.listdir(folder)
                            new_fnames = [
                                f
                                for f in file_list_1
                                if os.path.isfile(os.path.join(folder,f))
                                and f.lower().endswith((".png", ".jpg", ".jpeg", ".pdf"))
                            ]

                        count += 1
                    window.close()
                    #below statement is for updating values in previous window
                    return new_fnames

                except:
                    #name in use, try again
                    if new_file in os.listdir(folder):
                        sg.popup("This name is already in use")
                    #general catch in case program runs into unexpected scenario
                    else:
                        sg.popup("Something screwed up")

#===============================================================================

def photo_renamer():
    #empty file_list is made to prevent crashes encountered by pushing "OK" early.
    file_list = []

    #This sets up what will be on the left side of the window
    photo_column = [
        [sg.Text("Select source folder for photo(s)")],
        [sg.In(enable_events=True, readonly=True, k="-FOLDER-"),
        sg.FolderBrowse()],
        [sg.Text("Select photo(s) to rename:")],
        [sg.Listbox(values=file_list, select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED,
        enable_events=True, size=(40,20), k="-FILE LIST-")],
    ]

    #This sets up what will be on the right side of the window
    viewer_column = [
        [sg.Image(key="-IMAGE-")],
        [sg.Text("New photo name:")],
        [sg.In(key="-INPUT-", do_not_clear=False), sg.Button("OK")],
        [sg.Button("Mass rename"), sg.Button("Delete"), sg.Button("Upload")],
    ]

    #This sets up the window with a vertical line seperating the two sections
    layout = [
        [sg.Column(photo_column),
        sg.VSeperator(),
        sg.Column(viewer_column)]
    ]

    #This creates the new window, finalize makes it so that it doesn't throw
    #a warning when the window gets updated
    window = sg.Window(" ", layout)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            sys.exit()

        if event == "-FOLDER-":
            try:
                folder = values["-FOLDER-"]
                file_list = os.listdir(folder)
                fnames = []
                for f in file_list:
                    fnames= [
                        f
                        for f in file_list
                        if os.path.isfile(os.path.join(folder,f))
                        and f.lower().endswith((".png", ".jpg", ".jpeg", ".pdf"))
                    ]

            except:
                file_list = []
                fnames = []
            window["-FILE LIST-"].update(fnames)

        elif event == "-FILE LIST-":
            #The following block of code converts the picture from its original
            #size to a viewable thumbnail, while storing it in memory
            #The original file is unmodified during this conversion
            try:
                filename = os.path.join(
                    folder, values["-FILE LIST-"][0]
                )
                if filename.endswith(".pdf"):
                    image = Image.open("No preview available.png")

                else:
                    image = Image.open(filename)
                image.thumbnail((400, 400))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["-IMAGE-"].update(data=bio.getvalue())

            except:
                sg.popup("File list is empty")

        if event == "OK":
            if Input_field_check.input_field_check(values["-INPUT-"]) == True:
                pass

            else:
                #This sets up a check to verify the file name is not in use,
                #and the searches the input field to see if the file extension
                #was typed there. If it was, it only uses the input field, else
                #it adds the file_extension from the original file.
                try:
                    regex = r"(\.\w+)$"
                    file_extension = re.search(regex, values["-FILE LIST-"][0])
                    file_extension.groups()

                    if values["-INPUT-"].endswith(file_extension[0]) == True:
                        new_filename = os.path.join(folder, values["-INPUT-"])
                        os.rename(filename, new_filename)
                        file_list = os.listdir(folder)
                        fnames = [
                            f
                            for f in file_list
                            if os.path.isfile(os.path.join(folder, f))
                            and f.lower().endswith((".png", ".jpg", ".jpeg", ".pdf"))
                            ]
                        window["-FILE LIST-"].update(fnames)

                    else:
                        new_filename = os.path.join(folder, values["-INPUT-"]
                        + file_extension[0])
                        os.rename(filename, new_filename)
                        file_list = os.listdir(folder)
                        fnames = [
                            f
                            for f in file_list
                            if os.path.isfile(os.path.join(folder, f))
                            and f.lower().endswith((".png", ".jpg", ".jpeg", ".pdf"))
                            ]
                        window["-FILE LIST-"].update(fnames)

                except:
                    #exception block to verify unique names and to select a
                    #photo to begin renaming.
                    if values["-FOLDER-"] == "":
                        sg.popup("Please select a folder for files to be renamed", title=" ")

                    elif values["-INPUT-"] in file_list or values["-INPUT-"] \
                    + file_extension[0] in file_list:
                        sg.popup("This name is already in use", title =" ")

                    else:
                        sg.popup("Please select a file from the left", title =" ")

        if event == "Mass rename":
            file_list_mass = values["-FILE LIST-"]
            folder = values["-FOLDER-"]
            if file_list_mass == []:
                sg.popup("Please select photos for mass rename first")
            else:
                window["-FILE LIST-"].update(mass_renamer(folder, file_list_mass))

        if event == "Delete":
            file_list_delete = values["-FILE LIST-"]
            for file in file_list_delete:
                os.remove(os.path.join(folder, file))
            fnames_delete = [
                f
                for f in file_list
                if os.path.isfile(os.path.join(folder, f))
                and f.lower().endswith((".png", ".jpg", ".jpeg", ".pdf"))
            ]
            window["-FILE LIST-"].update(fnames_delete)

        if event == "Upload":
            if values["-FOLDER-"] == "":
                sg.popup("Please select a folder")
            else:
                File_uploader.Cred_check(folder, file_list)

#===============================================================================

def multiple_photo_folders_mover():
    #empty file_lists is made to prevent crashes encountered by pushing "OK" early.
    file_list_1 = []
    file_list = []
    fnames = []
    #defines left side of window
    column_1 = [
        [sg.Text("Select source folder")],
        [sg.In(enable_events=True, readonly=True, key="-FOLDER-"),
        sg.FolderBrowse()],
        [sg.Text("Select photo(s) to move:")],
        [sg.Listbox(values=file_list, select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED,
        enable_events=True, size=(40,20),key="-FILE LIST-")],
    ]
    #defines middle of window
    column_2 = [
        [sg.Text("Photo preview")],
        [sg.Image(key="-IMAGE-")],
        [sg.Button("Move >>")],
    ]
    #defines right side of window
    column_3 = [
        [sg.Text("Select destination folder")],
        [sg.In(enable_events=True, readonly=True, key="-FOLDER_1-"),
        sg.FolderBrowse()],
        [sg.Listbox(values=file_list_1, select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED,
        enable_events=True, size=(40,20), key="-FILE_LIST_1-")],
        [sg.Button("Done")],
    ]
    #puts all 3 parts together with seperators
    layout = [
        [sg.Column(column_1),
        sg.VSeperator(),
        sg.Column(column_2),
        sg.VSeperator(),
        sg.Column(column_3)]
    ]
    window = sg.Window(" ", layout)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        #code block for left folder selection files
        if event == "-FOLDER-":
            try:
                folder = values["-FOLDER-"]
                file_list = os.listdir(folder)
                for f in file_list:
                    fnames= [
                        f
                        for f in file_list
                        if os.path.isfile(os.path.join(folder,f))
                        and f.lower().endswith((".png", ".jpg", ".jpeg", ".pdf"))
                    ]

            except:
                file_list = []
            window["-FILE LIST-"].update(fnames)

        elif event == "-FILE LIST-":
            #The following block of code converts the picture from its original
            #size to a viewable thumbnail, while storing it in memory
            #The original file is unmodified during this conversion.
            #If file is .pdf, displays placeholder image.
            try:
                filename = os.path.join(
                    folder, values["-FILE LIST-"][0]
                )
                if filename.endswith(".pdf"):
                    image = Image.open("No preview available.png")
                else:
                    image = Image.open(filename)
                image.thumbnail((400, 400))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["-IMAGE-"].update(data=bio.getvalue())

            except:
                sg.popup("Left file list is empty")

        elif event == "-FILE_LIST_1-":
            #The following block of code converts the picture from its original
            #size to a viewable thumbnail, while storing it in memory
            #The original file is unmodified during this conversion
            #If file is .pdf, displays placeholder image.
            try:
                filename = os.path.join(
                    folder_1, values["-FILE_LIST_1-"][0]
                )
                if filename.endswith(".pdf"):
                    image = Image.open("No preview available.png")
                else:
                    image = Image.open(filename)
                image.thumbnail((400, 400))
                bio = io.BytesIO()
                image.save(bio, format = "PNG")
                window["-IMAGE-"].update(data=bio.getvalue())

            except:
                sg.popup("Right file list is empty")
        #code block for right folder selection files
        elif event == "-FOLDER_1-":
            folder_1 = values["-FOLDER_1-"]
            fnames_1 = []

            try:
                file_list_1 = os.listdir(folder_1)
                for f_1 in file_list_1:
                    fnames_1= [
                        f_1
                        for f_1 in file_list_1
                        if os.path.isfile(os.path.join(folder_1, f_1))
                        and f_1.lower().endswith((".png", ".jpg", ".jpeg", ".pdf"))
                        ]

            except:
                file_list_1 = []
            window["-FILE_LIST_1-"].update(fnames_1)
        #code block for moving files from left folder to right folder.
        elif event == "Move >>":
            if values["-FOLDER-"] == "" or values["-FOLDER_1-"] == "":
                sg.popup("Please select a folder before moving photos!")
            #moves file from left folder to right folder
            else:
                for file in values["-FILE LIST-"]:
                    filename_1 = os.path.join(folder, file)
                    new_filename_1 = os.path.join(folder_1, file)
                    os.replace(filename_1,new_filename_1)
                #update each folder list in window
                try:
                    folder = values["-FOLDER-"]
                    file_list = os.listdir(folder)

                    for f in file_list:
                        fnames= [
                            f
                            for f in file_list
                            if os.path.isfile(os.path.join(folder,f))
                            and f.lower().endswith((".png", ".jpg", ".jpeg", ".pdf"))
                        ]
                    folder_1 = values["-FOLDER_1-"]
                    file_list_1 = os.listdir(folder_1)

                    for f_1 in file_list_1:
                        fnames_1= [
                            f_1
                            for f_1 in file_list_1
                            if os.path.isfile(os.path.join(folder_1, f_1))
                            and f_1.lower().endswith((".png", ".jpg", ".jpeg", ".pdf"))
                            ]

                except:
                    file_list = []
                    file_list_1 = []

                window["-FILE LIST-"].update(fnames)
                window["-FILE_LIST_1-"].update(fnames_1)
        #checks path and proceeds to next function based on original criteria.
        elif event == "Done":
            window.close()
            photo_renamer()

#===============================================================================

def multiple_photo_folders(YES_1_check_value):
    #define layout for folder creation Window
    layout = [
        [sg.Text("Where are folders going to be created?"),
        sg.In("", readonly=True, k="-FOLDER-"),
        sg.FolderBrowse()],
        [sg.Text("How many folders need to be created?"),
        sg.Input("", k="-IN-")],
        [sg.Button("OK")],
    ]
    window = sg.Window(" ", layout)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        #first 2 cases as defined, only except # and folder.
        if event == "OK":
            if values["-IN-"].strip().isdigit() != True:
                sg.popup("Please enter a number", title=" ")

            elif values["-FOLDER-"] == "":
                sg.popup("Please select a folder before continuing", title=" ")

            else:
                #checks path and proceeds to correct function if folders needed is 0.
                window.close()
                if int(values["-IN-"]) == 0 and YES_1_check_value == True:
                    multiple_photo_folders_mover()

                elif int(values["-IN-"]) == 0 and YES_1_check_value == False:
                    photo_renamer()

                else:
                    #for loop iterates to max value input in folders desired field
                    for folder_num in range(int(values["-IN-"])):
                        layout_1 = [
                            [sg.Text("Folder {} name:".format(folder_num + 1)),
                            sg.Input("", k="-IN_1-")],
                            [sg.Button("OK")],
                        ]
                        window_1 = sg.Window(" ", layout_1)
                        #creates each folder in a separate window, one at a time
                        while True:
                            event_1, values_1 = window_1.read()
                            if event_1 == "Exit" or event_1 == sg.WIN_CLOSED:
                                break

                            if event_1 == "OK":
                                if Input_field_check.input_field_check(values_1["-IN_1-"]) == True:
                                    pass

                                else:
                                    #checks file list to make sure folder
                                    #name isn't already in use.
                                    folder = values["-FOLDER-"]
                                    file_list = os.listdir(folder)
                                    for i in range(len(file_list)):
                                        file_list[i] = file_list[i].lower()
                                    if values_1["-IN_1-"].lower() in file_list:
                                        sg.popup("Name already in use, choose another")

                                    else:
                                        window_1.close()
                                        os.mkdir(folder + "/" + values_1["-IN_1-"])
                    #checks original path and continues based on that
                    if YES_1_check_value == True:
                        multiple_photo_folders_mover(YES_check_value)

                    else:
                        photo_renamer()

#===============================================================================

if __name__ == "__main__":
    main()

##TO DO:
#add ability to move other file types, if desired. No photo preview would be available.
    #^added .pdf and no preview available file to support this
#possibly add a file conversion or resizer ability, if desired
#   ^ this would be good if file sizes need to be reduced to under x MB
