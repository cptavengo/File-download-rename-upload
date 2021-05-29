import PySimpleGUI as sg
import os.path
import os
import sys
import re
import io
from PIL import Image
import File_uploader
import Input_field_check

#===============================================================================

def main():
    #defines layout for first window of module
    layout = [
        [sg.Text("Would you like to rename photos?"),
        sg.Checkbox("Yes", key="-YES-"), sg.Checkbox("No", k="-NO-")],
        [sg.Text("Are multiple folders needed for renaming?"),
        sg.Checkbox("Yes", k="-YES_1-"), sg.Checkbox("No", k="-NO_1-")],
        [sg.Text("Is multiple folder move mode needed?"),
        sg.Checkbox("Yes", k="-YES_2-"), sg.Checkbox("No", k="-NO_2-")],
        [sg.Button("OK")],
    ]

    window = sg.Window(" ", layout)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == "OK":
            #defines what happens for first row of checkboxes
            if values["-YES-"] == True and values["-NO-"] == False:
                if values["-YES_1-"] == True and values["-NO_1-"] == False:
                    window.close()
                    multiple_photo_folders(values["-NO-"])

                if values["-NO_1-"] == True and values["-YES_1-"] == False:
                    if values["-YES_2-"] == False:
                        window.close()
                        photo_renamer()

                    else:
                        window.close()
                        multiple_photo_folders_mover(values["-NO-"])

                if values["-NO_1-"] == True and values["-YES_1-"] == True:
                    sg.popup("Please on select yes OR no.")

            if values["-NO-"] == True and values["-YES-"] == False:
                if values["-YES_1-"] == True and values["-NO_1-"] == False:
                    window.close()
                    multiple_photo_folders(values["-NO_2-"])

                if values["-NO_1-"] == True and values["-YES_1-"] == False:
                    window.close()
                    no_photo_renamer()

            if values["-NO-"] == True and values["-YES-"] == True:
                sg.popup("Please on select yes OR no.")

#===============================================================================

def mass_renamer(list_files, folder):
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
            if Input_field_check.input_field_check(values["-IN-"]) == False:
                pass

            else:
                try:
                    count = 1

                    for file in list_files:
                        regex = r"(\.\w+)$"
                        file_extension = re.search(regex, file)
                        file_extension.groups()

                        if values["-IN-"].endswith(file_extension[0]) == True:
                            filename = os.path.join(folder + "\\" + file)
                            values["-IN-"] = values["-IN-"].replace(file_extension[0], "")
                            new_file = values["-IN-"] + "(" + str(count) + ")" + file_extension[0]
                            new_filename = os.path.join(folder, new_file)
                            os.rename(filename, new_filename)
                            file_list = os.listdir(folder)
                            new_fnames = [
                                f
                                for f in file_list
                                if os.path.isfile(os.path.join(folder,f))
                                and f.lower().endswith((".png", ".jpg", ".jpeg", ".pdf"))
                            ]

                        else:
                            filename = os.path.join(folder + "\\" + file)
                            new_file = values["-IN-"] + "(" + str(count) + ")" + file_extension[0]
                            new_filename = os.path.join(folder, new_file)
                            os.rename(filename, new_filename)
                            file_list = os.listdir(folder)
                            new_fnames = [
                                f
                                for f in file_list
                                if os.path.isfile(os.path.join(folder,f))
                                and f.lower().endswith((".png", ".jpg", ".jpeg", ".pdf"))
                            ]

                        count += 1
                    window.close()
                    return new_fnames

                except:
                    if new_file in os.listdir(folder):
                        sg.popup("This name is already in use")
                    else:
                        sg.popup("Something screwed up")

#===============================================================================

def no_photo_renamer():
    file_list = []
    layout = [
        [sg.Text("Select upload source folder:")],
        [sg.In(enable_events=True, readonly=True, k="-FOLDER-"), sg.FolderBrowse()],
        [sg.Button("OK")],
    ]
    window = sg.Window(" ", layout)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event == "OK":
            if values["-FOLDER-"] == "":
                sg.popup("Please select a folder")
            else:
                folder = values["-FOLDER-"]
                file_list = os.listdir(folder)
                File_uploader.photo_uploader(folder, file_list)

#===============================================================================

def photo_renamer():
    file_list = []

    #This sets up what will be on the left side of the window
    photo_column = [
        [sg.Text("Select source folder for photo(s)")],
        [sg.In(enable_events=True, readonly=True, key="-FOLDER-"),
        sg.FolderBrowse()],
        [sg.Text("Select photo(s) to rename:")],
        [sg.Listbox(values=file_list, select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED,
        enable_events=True, size=(40,20),key="-FILE LIST-")],
    ]

    #This sets up what will be on the right side of the window
    viewer_column = [
        [sg.Image(key="-IMAGE-")],
        [sg.Text("New photo name:")],
        [sg.In(key="-INPUT-", do_not_clear=False), sg.Button("OK")],
        [sg.Button("Mass rename"), sg.Button("Done")],
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
                pass
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
            list_files = values["-FILE LIST-"]
            folder = values["-FOLDER-"]
            if list_files == []:
                sg.popup("Please select photos for mass rename first")
            else:
                window["-FILE LIST-"].update(mass_renamer(list_files, folder))

        if event == "Done":
            if values["-FOLDER-"] == "":
                sg.popup("Please select a folder")
            else:
                File_uploader.photo_uploader(folder, file_list)

#===============================================================================

def multiple_photo_folders_mover(NO_check_value):
    file_list_1 = []
    file_list = []

    column_1 = [
        [sg.Text("Select source folder")],
        [sg.In(enable_events=True, readonly=True, key="-FOLDER-"),
        sg.FolderBrowse()],
        [sg.Text("Select photo(s) to move:")],
        [sg.Listbox(values=file_list, select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED,
        enable_events=True, size=(40,20),key="-FILE LIST-")],
    ]
    column_2 = [
        [sg.Text("Photo preview")],
        [sg.Image(key="-IMAGE-")],
        [sg.Button("Move >>")],
    ]
    column_3 = [
        [sg.Text("Select destination folder")],
        [sg.In(enable_events=True, readonly=True, key="-FOLDER_1-"),
        sg.FolderBrowse()],
        [sg.Listbox(values=file_list_1, select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED,
        enable_events=True, size=(40,20), key="-FILE_LIST_1-")],
        [sg.Button("Done")],
    ]

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
                pass

        elif event == "-FILE_LIST_1-":
            #The following block of code converts the picture from its original
            #size to a viewable thumbnail, while storing it in memory
            #The original file is unmodified during this conversion
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
                pass

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

        elif event == "Move >>":
            if values["-FOLDER-"] == "" or values["-FOLDER_1-"] == "":
                sg.popup("Please select a folder before moving photos!")
            else:
                for file in values["-FILE LIST-"]:
                    filename_1 = os.path.join(folder, file)
                    new_filename_1 = os.path.join(folder_1, file)
                    os.replace(filename_1,new_filename_1)

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

        elif event == "Done":
            if NO_check_value == True:
                window.close()
                photo_renamer()

            elif NO_check_value == False:
                window.close()
                no_photo_renamer()

#===============================================================================

def multiple_photo_folders(NO_check_value):
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

        if event == "OK":
            if values["-IN-"].strip().isdigit() != True:
                sg.popup("Please enter a number", title=" ")

            elif values["-FOLDER-"] == "":
                sg.popup("Please select a folder before continuing", title=" ")

            else:
                window.close()
                #for loop iterates to max value input in folders desired field
                if int(values["-IN-"]) == 0 and NO_check_value == False:
                    multiple_photo_folders_mover(NO_check_value)

                elif int(values["-IN-"]) == 0 and NO_check_value == True:
                    folder = values["-FOLDER-"]
                    file_list = os.listdir(folder)
                    File_uploader.photo_uploader(folder, file_list)

                else:
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
                                sys.exit()

                            if event_1 == "OK":
                                if Input_field_check.input_field_check(values_1["-IN_1-"]) == True:
                                    pass

                                else:
                                    try:
                                        folder = values["-FOLDER-"]
                                        if values_1["-IN_1-"] in os.listdir(folder):
                                            sg.popup("Name already in use, choose another")

                                        else:
                                            window_1.close()
                                            os.mkdir(folder + "/" + values_1["-IN_1-"])
                                            multiple_photo_folders_mover(NO_check_value)

                                    except:
                                        sg.popup("An error has occurred")

#===============================================================================

if __name__ == "__main__":
    main()

##TO DO:
#add ability to move other file types, if desired. No photo preview would be available.
    #^added .pdf and no preview available file to support this
#possibly add a file conversion or resizer ability, if desired
#   ^ this would be good if file sizes need to be reduced to under x MB
