import requests, os.path, Checks, json, sys, re, Photo_renamer
from googleapiclient.discovery import build
import PySimpleGUI as sg

#===============================================================================

def main():
    menu_def = [
        ["File", ["File Mover", "Photo Renamer",
        "Folder Creator", "---", "Properties", "Exit"]],
    ]

    section1 = [
        [sg.In(size=(9,20), readonly=True, k="-Calendar-"),
        sg.CalendarButton("Single date", format="%Y-%m-%d",
        close_when_date_chosen=False)]
    ]

    section2 = [
        [sg.In(size=(9,20), readonly=True, k="-Calendar_1-"),
        sg.CalendarButton("Begin date",
        format="%Y-%m-%d", close_when_date_chosen=False),
        sg.In(size=(9,20), readonly=True, k="-Calendar_2-"),
        sg.CalendarButton("End date",
        format="%Y-%m-%d", close_when_date_chosen=False)],
    ]

    layout = [
        [sg.Menu(menu_def)],
        [sg.Text("Select destination for download")],
        [sg.In(enable_events=True, readonly=True, k="-FOLDER-"),
        sg.FolderBrowse()],
        [sg.Radio("single date", group_id=1, k="-Single_date-", enable_events=True),
        sg.Radio("date range", k="-Date_range-", enable_events=True, group_id=1)],
        [collapse(section1, "-Sec1-")],
        [collapse(section2, "-Sec2-")],
        [sg.Button("Download"), sg.Button("Photo move and/or rename")]
    ]

    window = sg.Window(" ", layout)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            sys.exit()

        if event == "-Single_date-":
            opened1, opened2 = False, True
            opened1 = not opened1
            opened2 = not opened2
            window["-Sec1-"].update(visible = opened1)
            window["-Sec2-"].update(visible = opened2)

        if event == "-Date_range-":
            opened1, opened2 = True, False
            opened1 = not opened1
            opened2 = not opened2
            window["-Sec1-"].update(visible = opened1)
            window["-Sec2-"].update(visible = opened2)

        if event == "Download":
            if values["-FOLDER-"] == "":
                sg.popup("Please select a folder to download to")

            elif values["-Single_date-"] == True:
                if values["-Calendar-"] == "":
                    sg.popup("Please select a date")

                else:
                    date_split = values["-Calendar-"].split("-")
                    Single_date_photo(Checks.Cred_check(), date_split[0], \
                    date_split[1], date_split[2], values["-FOLDER-"])

            elif values["-Date_range-"] == True:
                if values["-Calendar_1-"] == "" or values["-Calendar_2-"] == "":
                    sg.popup("Please select dates from both calendars")

                elif values["-Calendar_1-"] > values["-Calendar_2-"]:
                    sg.popup("End date and start date reversed")

                else:
                    date_split_1 = values["-Calendar_1-"].split("-")
                    date_split_2 = values["-Calendar_2-"].split("-")
                    Date_range_photo(Checks.Cred_check(),
                    date_split_1[0], date_split_2[0], date_split_1[1],
                    date_split_2[1], date_split_1[2], date_split_2[2],
                    values["-FOLDER-"])

        if event == "Photo move and/or rename":
            window.close()
            Photo_renamer.main()

        if event == "File Mover":
            window.close()
            Photo_renamer.multiple_photo_folders_mover()

        if event == "Folder Creator":
            window.close()
            Photo_renamer.multiple_photo_folders(False)

        if event == "Photo Renamer":
            window.close()
            Photo_renamer.photo_renamer()

        if event == "Properties":
            sg.popup("Future button currently not working")


#===============================================================================

#Function below is from PySimpleGUI documentation cookbook, recipe for creating
#collapsed sections in a window.
def collapse(layout, key):
    return sg.pin(sg.Column(layout, visible=False, key=key))

#===============================================================================

def Single_date_photo(creds, year, month, day, destination_folder):
    PHOTOS = build("photoslibrary", "v1", static_discovery=False, credentials=creds)
    response = PHOTOS.mediaItems().search(body={"filters":{"dateFilter": \
    {"dates":[{"day":day, "month":month, "year":year}]}}}).execute()
    items = response.get("mediaItems", [])

    layout_1 = [
        [sg.Text("Downloading files now...")],
        [sg.ProgressBar(len(items), orientation="h", \
        size=(20,20), k="-PROG-")],
        [sg.Text(k="-TEXT-", size=(20,0))]
    ]
    window_1 = sg.Window(" ", layout_1)
    i = 1

    for item in items:
        event_1, values_1 = window_1.read(timeout=10)
        download_photo = item["baseUrl"] + "=d"
        filename = item["filename"]
        photo_request = requests.get(download_photo)
        with open(os.path.join(destination_folder, filename), "wb") as photo:
            photo.write(photo_request.content)
            photo.close()

        window_1["-PROG-"].update(i)
        window_1["-TEXT-"].update("{} / {} files uploaded" \
        .format(str(i), str(len(items))))
        i += 1
        if event_1 == "Exit" or event_1 == sg.WIN_CLOSED:
            break
    window_1.close()
    sg.popup("Files downloaded to {}".format(destination_folder))

#===============================================================================

def Date_range_photo(creds, year1, year2, month1, month2, day1, day2, destination_folder):
    PHOTOS = build("photoslibrary", "v1", static_discovery=False, credentials=creds)
    response = PHOTOS.mediaItems().search(body={"filters":{"dateFilter": \
    {"ranges": [{"startDate": {"year": year1, "month": month1, "day": day1}, \
    "endDate": {"year": year2, "month": month2, "day": day2}}]}}}).execute()
    items = response.get("mediaItems", [])

    layout_1 = [
        [sg.Text("Downloading files now...")],
        [sg.ProgressBar(len(items), orientation="h", \
        size=(20,20), k="-PROG-")],
        [sg.Text(k="-TEXT-", size=(20,0))]
    ]
    window_1 = sg.Window(" ", layout_1)
    i = 1

    for item in items:
        event_1, values_1 = window_1.read(timeout=10)
        download_photo = item["baseUrl"] + "=d"
        filename = item["filename"]
        photo_request = requests.get(download_photo)
        with open(os.path.join(destination_folder, filename), "wb") as photo:
            photo.write(photo_request.content)
            photo.close()

        window_1["-PROG-"].update(i)
        window_1["-TEXT-"].update("{} / {} files uploaded" \
        .format(str(i), str(len(items))))
        i += 1
        if event_1 == "Exit" or event_1 == sg.WIN_CLOSED:
            break
    window_1.close()
    sg.popup("Files downloaded to {}".format(destination_folder))

#===============================================================================

if __name__ == "__main__":
    main()
