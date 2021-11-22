import requests, os.path, Checks, json, sys, re, Photo_renamer
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

def main():
    menu_def = [
        ["File", ["File Mover", "File Renamer",
        "Folder Creator", "---", "Properties", ["Themes", "Image Size"], "Exit"]],
    ]

    section1 = [
        [sg.In(size=(9,20), readonly=True, k="-Calendar-",
        disabled_readonly_background_color=sg.theme_input_background_color()),
        sg.CalendarButton("Single date", format="%Y-%m-%d",
        close_when_date_chosen=False)]
    ]

    section2 = [
        [sg.In(size=(9,20), readonly=True, k="-Calendar_1-",
        disabled_readonly_background_color=sg.theme_input_background_color()),
        sg.CalendarButton("Begin date", format="%Y-%m-%d",
        close_when_date_chosen=False),
        sg.In(size=(9,20), readonly=True, k="-Calendar_2-",
        disabled_readonly_background_color=sg.theme_input_background_color()),
        sg.CalendarButton("End date", format="%Y-%m-%d",
        close_when_date_chosen=False)],
    ]

    layout = [
        [sg.Menu(menu_def)],
        [sg.Text("Select destination for download")],
        [sg.In(enable_events=True, readonly=True, k="-FOLDER-",
        disabled_readonly_background_color=sg.theme_input_background_color()),
        sg.FolderBrowse()],
        [sg.Radio("single date", group_id=1, k="-Single_date-", enable_events=True),
        sg.Radio("date range", k="-Date_range-", enable_events=True, group_id=1)],
        [collapse(section1, "-Sec1-")],
        [collapse(section2, "-Sec2-")],
        [sg.Button("Download"), sg.Button("File move and/or rename")]
    ]

    window = sg.Window(" ", layout, icon=icon)

    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            sys.exit()

        if event == "-Single_date-":
            opened1, opened2 = True, False
            window["-Sec1-"].update(visible=opened1)
            window["-Sec2-"].update(visible=opened2)

        if event == "-Date_range-":
            opened1, opened2 = False, True
            window["-Sec1-"].update(visible=opened1)
            window["-Sec2-"].update(visible=opened2)

        if event == "Download":
            if values["-FOLDER-"] == "":
                sg.popup("Please select a folder to download to", title=" ",
                icon=icon)

            elif values["-Single_date-"] is True:
                if values["-Calendar-"] == "":
                    sg.popup("Please select a date", title=" ", icon=icon)

                else:
                    date_split = values["-Calendar-"].split("-")
                    creds = Checks.Cred_check()
                    if creds is None:
                        continue

                    else:
                        Single_date_photo(creds, date_split[0], \
                        date_split[1], date_split[2], values["-FOLDER-"])

            elif values["-Date_range-"] is True:
                if values["-Calendar_1-"] == "" or values["-Calendar_2-"] == "":
                    sg.popup("Please select dates from both calendars",
                    title=" ", icon=icon)

                elif values["-Calendar_1-"] > values["-Calendar_2-"]:
                    sg.popup("End date and start date reversed", title=" ",
                    icon=icon)

                else:
                    date_split_1 = values["-Calendar_1-"].split("-")
                    date_split_2 = values["-Calendar_2-"].split("-")
                    Date_range_photo(Checks.Cred_check(),
                    date_split_1[0], date_split_2[0], date_split_1[1],
                    date_split_2[1], date_split_1[2], date_split_2[2],
                    values["-FOLDER-"])

        if event == "File move and/or rename":
            window.close()
            Photo_renamer.main()

        if event == "File Mover":
            window.close()
            Photo_renamer.multiple_photo_folders_mover()

        if event == "Folder Creator":
            window.close()
            Photo_renamer.multiple_photo_folders(False)

        if event == "File Renamer":
            window.close()
            Photo_renamer.photo_renamer()

        if event == "Themes":
            properties()
            window.close()
            main()

        if event == "Image Size":
            imageSize()

#===============================================================================

#Function below is from PySimpleGUI documentation cookbook, recipe for creating
#collapsed sections in a window.
def collapse(layout, key):
    return sg.pin(sg.Column(layout, visible=False, key=key))

#===============================================================================

def Single_date_photo(creds, year, month, day, destination_folder):
    PHOTOS = build("photoslibrary", "v1", static_discovery=False,
    credentials=creds)
    nextPageToken = "empty"
    items = []

    while nextPageToken != "":
        if nextPageToken == "empty":
            nextPageToken = ""

        else:
            nextPageToken

        response = PHOTOS.mediaItems().search(body={"filters":{"dateFilter": \
        {"dates":[{"day":day, "month":month, "year":year}]}},
        "pageToken": nextPageToken}).execute()

        for item in response.get("mediaItems", []):
            items.append(item)
        nextPageToken = response.get("nextPageToken", "")

    layout_1 = [
        [sg.Text("Downloading photos now...")],
        [sg.ProgressBar(len(items), orientation="h", \
        size=(20,20), k="-PROG-")],
        [sg.Text(k="-TEXT-", size=(20,0))]
    ]

    window_1 = sg.Window(" ", layout_1, icon=icon)

    for i, item in enumerate(items, 1):
        event_1, values_1 = window_1.read(timeout=10)
        download_photo = item["baseUrl"] + "=d"
        filename = item["filename"]
        photo_request = requests.get(download_photo)
        with open(os.path.join(destination_folder, filename), "wb") as photo:
            photo.write(photo_request.content)
            photo.close()

        window_1["-PROG-"].update(i)
        window_1["-TEXT-"].update("{} / {} photos downloaded" \
        .format(str(i), str(len(items))))

        if event_1 == "Exit" or event_1 == sg.WIN_CLOSED:
            break

    window_1.close()
    sg.popup("Photos downloaded to {}".format(destination_folder), title=" ",
    icon=icon)

#===============================================================================

def Date_range_photo(creds, year1, year2, month1, month2, day1, day2, destination_folder):
    PHOTOS = build("photoslibrary", "v1", static_discovery=False,
    credentials=creds)
    nextPageToken = "empty"
    items = []

    while nextPageToken != "":
        if nextPageToken == "empty":
            nextPageToken = ""

        else:
            nextPageToken

        response = PHOTOS.mediaItems().search(body={"filters":{"dateFilter": \
        {"ranges": [{"startDate": {"year": year1, "month": month1, "day": day1},
        "endDate": {"year": year2, "month": month2, "day": day2}}]}},
        "pageToken": nextPageToken}).execute()

        for item in response.get("mediaItems", []):
            items.append(item)
        nextPageToken = response.get("nextPageToken", "")

    layout_1 = [
        [sg.Text("Downloading photos now...")],
        [sg.ProgressBar(len(items), orientation="h", \
        size=(20,20), k="-PROG-")],
        [sg.Text(k="-TEXT-", size=(20,0))]
    ]

    window_1 = sg.Window(" ", layout_1, icon=icon)

    for i, item in enumerate(items, 1):
        event_1, values_1 = window_1.read(timeout=10)
        download_photo = item["baseUrl"] + "=d"
        filename = item["filename"]
        photo_request = requests.get(download_photo)
        with open(os.path.join(destination_folder, filename), "wb") as photo:
            photo.write(photo_request.content)
            photo.close()

        window_1["-PROG-"].update(i)
        window_1["-TEXT-"].update("{} / {} photos downloaded" \
        .format(str(i), str(len(items))))

        if event_1 == "Exit" or event_1 == sg.WIN_CLOSED:
            break

    window_1.close()
    sg.popup("Photos downloaded to {}".format(destination_folder), title=" ",
    icon=icon)

#===============================================================================

#Color chooser is modified from PySimpleGUI recipe for theme viewer.
def properties():
    layoutTheme = [
        [sg.Text("Choose a theme to apply to all elements and windows")],
        [sg.Listbox(values=sg.theme_list(), size=(20,12), k="-THEME-",
        enable_events=True)], [sg.Button("OK")]
    ]

    windowTheme = sg.Window(" ", layoutTheme, icon=icon)

    while True:
        eventTheme, valuesTheme = windowTheme.read()
        if eventTheme == "Exit" or eventTheme == sg.WIN_CLOSED:
            if os.path.exists("Theme.json"):
                with open("Theme.json", "r") as Theme:
                    windowTheme = json.load(Theme)
                sg.theme(windowTheme)
            break

        if eventTheme == "-THEME-":
            sg.theme(valuesTheme["-THEME-"][0])
            layoutTest = [
                [sg.Text("This is {}".format(valuesTheme["-THEME-"][0]))],
                [sg.In()],
                [sg.Button("OK")]
            ]

            windowTest = sg.Window(" ", layoutTest, icon=icon)
            while True:
                eventTest, valuesTest = windowTest.read()
                if eventTest == "Exit" or eventTest == sg.WIN_CLOSED:
                    break

                if eventTest == "OK":
                    windowTest.close()

        if eventTheme == "OK":
            windowTheme.close()
            sg.popup("Theme changed to {}."
            .format(valuesTheme["-THEME-"][0]), title=" ", icon=icon)
            theme = {"Theme": valuesTheme["-THEME-"][0]}

            if os.path.exists("Properties.json"):
                with open("Properties.json") as filetheme:
                    old_theme = json.load(filetheme)

                old_theme["Theme"] = valuesTheme["-THEME-"][0]
                with open("Properties.json", "w") as filetheme:
                    json.dump(old_theme, filetheme, indent=1)

            else:
                with open("Properties.json", "w") as new_theme:
                    json.dump(theme, new_theme, indent=1)

#===============================================================================

def imageSize():
    layoutSize = [
        [sg.Text("Choose either small or large sizes for images")],
        [sg.Radio("Small", group_id=1, k="-small-"),
        sg.Radio("Large", group_id=1, k="-large-")],
        [sg.Button("OK")]
    ]

    windowSize = sg.Window(" ", layoutSize, icon=icon)
    while True:
        eventSize, valuesSize = windowSize.read()
        if eventSize == "Exit" or eventSize == sg.WIN_CLOSED:
            break

        elif eventSize == "OK":
            if valuesSize["-small-"] is True:
                size = {"Size": (400, 400)}

            else:
                size = {"Size": (800, 800)}

            windowSize.close()
            if os.path.exists("Properties.json"):
                with open("Properties.json") as fsize:
                    old_size = json.load(fsize)

                old_size["Size"] = size["Size"]
                with open("Properties.json", "w") as fsize:
                    json.dump(old_size, fsize, indent=1)

            else:
                with open("Properties.json", "w") as fsize:
                    json.dump(size, fsize, indent=1)


#===============================================================================
if __name__ == "__main__":
    main()
