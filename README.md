<h1> Introduction, state of project, possible updates </h1>

This repository contains all my file manipulation Python files. The program downloads photos from Google Photos, manipulates file names, can add folders, move files to new folders, and then upload files to Google Drive. This primarily was a coding practice for me. The major restriction that I had in place for myself was that the program(s) use PySimpleGUI to view photos, file names, and folder names. As of 11/7/2021, the program is in a satisfactory state, as the program does all the things I wanted it to do when I started. There are a few file type additions I will add at some point (.doc/.docx and .xls/.xlsx are the ones that spring to mind). The tool even has customization options for changing font/background colors, and will remember the settings for future runs!

<h1> Program in action </h1>

1. [Photo download](#Photodownload)
2. [New folder creation](#newfoldercreation)
3. [Moving files](#movingfiles)
4. [Renaming files](#renamingfiles)
5. [Uploading files](#uploadingfiles)
6. [File menu](#menu)

Here is an example of the different parts of the program from start to finish. 

One thing to note, since this program interacts with the Google Photos and Drive APIs, the program must be added to the Google Developer dashboard and the Credentials.json downloaded to the folder containing the program. This is how the program creates and reads the tokens needed to allow access to Photos and Drive. The user will be prompted to reallow the program access to Photos and Drive periodically to refresh the tokens.

<a name="Photodownload"> </a>

<h2> Photo download </h2>

The program begins in this first window:

![Beginning window](https://user-images.githubusercontent.com/81875107/140841843-9505e51b-ee49-4596-a751-2324c7568e03.png)

where the user is prompted to enter a folder on the local host to download photos to, and to select from either a single date:

![Single date selection](https://user-images.githubusercontent.com/81875107/140841881-926d7c9e-76fb-4cda-a8d5-c7bd84570cbb.png)

or a date range, where each of the buttons opens a calendar as shown above for each prompt:

![Date range selection](https://user-images.githubusercontent.com/81875107/140841914-cdd97e36-a95e-4534-a6ad-033fdceb8af2.png)

After the user has selected a folder and date(s) the program calls the Google Photos API with the date filter input by the user for all photos in the range. The program then updates the user by showing a progress window for how many photos will be downloaded and how many have currently been downloaded:

![Download with a progress bar](https://user-images.githubusercontent.com/81875107/140841939-7b4a94f4-4306-4e53-a3f0-3fb97ac37e39.png)

<a name="newfoldercreation"> </a>

<h2> New folder creation </h2>

After the user is done using the download tool and selects the correct button, the user is prompted for new inputs:

![Program flow after download](https://user-images.githubusercontent.com/81875107/140841981-e8a22d53-4ff9-4204-af45-7f3145925b9e.png)

Selecting yes for the first radio brings the user to a window as shown below. The user is asked for a location to make new folders, and how many should be created in the new location. If an entry of 0 is received, the program will continue on the flow without prompting to create new folders.

![Folder creation option](https://user-images.githubusercontent.com/81875107/140842019-f1b2d423-1967-416d-ba87-78ef0c568a00.png)

<a name="movingfiles"> </a>

<h2> Moving files </h2>

Here is the window for moving files from one folder to another (for example, moving files from a USB drive to a storage folder on the user's PC):

![File mover example](https://user-images.githubusercontent.com/81875107/140842053-c529d53a-f319-4a85-a816-e64ad939a7d0.png)

The window requires the user to input a source folder and a destination folder. Then the .jpg, .png, .jpeg, and .pdf files are shown in each of the folders. The user can select individual or multiple (using CTRL if needed) files to move to the destination folder. Image files are shown in the middle, while .pdf shows a generic image file. Clicking __Move >>__ copies the file to the destination folder and then deletes it from the first folder.

![File mover example 2](https://user-images.githubusercontent.com/81875107/140842070-71aee877-8e46-490e-9ae2-1e9b7426213a.png)

<a name="renamingfiles"> </a>

<h2> Renaming files </h2>

Renaming files is accomplished in this window:

![File renamer example](https://user-images.githubusercontent.com/81875107/141379711-8c847b92-6f75-4acf-8ff0-1bfc481a427b.png)

which updates the file list after a name has been entered:

![File renamed](https://user-images.githubusercontent.com/81875107/141379754-3e92bd25-78a8-4308-a1b0-d3d22378b172.png)

Multiple files can be updated at once using the __Mass rename__ button:

![Mass rename example](https://user-images.githubusercontent.com/81875107/141379828-c671e280-55a3-4142-bc16-75ad73268657.png)

which results in files following a format like below:

![After mass rename](https://user-images.githubusercontent.com/81875107/141379863-2f62b2a0-cb37-4f63-8e3b-dd655812634e.png)

The delete button does exactly what it says, it deletes the file from the local host. It does not move it to a recycle area, it is gone. Delete has a confirmation before the file is deleted, as shown below:

![Delete confirmation](https://user-images.githubusercontent.com/81875107/141380009-f1ebb0af-2098-4d2a-aa0e-d8fe20607aef.png)

Which results in the file being removed and the viewer being cleared:

![File deleted](https://user-images.githubusercontent.com/81875107/141380099-3ea2decf-6fc9-4a22-af36-7ccd7a05351e.png)

The two rotate buttons, Rotate &#x2B6E; and Rotate &#x2B6F;, rotate the image clockwise and counterclockwise 90&#x00B0; in the corresponding direction.

Rotate &#x2B6E;:

![Rotate 90 clockwise](https://user-images.githubusercontent.com/81875107/141381578-8b1a6904-a891-4989-97a7-1d6f3f442c82.png)

Rotate &#x2B6F;:

![Rotate 90 counterclockwise](https://user-images.githubusercontent.com/81875107/141381598-74be72ed-9f83-4cce-a658-45d5e78c6e65.png)

Upload moves on to the last major part of the program.

<a name ="uploadingfiles"> </a>

<h2> Uploading files </h2>

The program prompts for user input on several areas for upload. Shared flags the files to be visible by other collaborators for shared Drives, and not sharing causes the file(s) to be uploaded to the user's Drive instead. Note that the file renamer portion stays open while the upload program is running so that the user can switch folders to upload more files, if desired.

![File uploader window](https://user-images.githubusercontent.com/81875107/141379918-53a75328-dee8-46dd-ae42-97f0742f7476.png)

Below shows the windows opened while uploading files. The background window is the list of Drive folders the user can upload to. This list can be shortened to include commonly used folders by editting the .json file that is created when gathering all the folders the first time. Otherwise, the program just uses the full list to help reduce the amount of time it takes to look for Drive folders.

![File uploader windows](https://user-images.githubusercontent.com/81875107/140842246-18b5e484-3b84-4a0a-8486-20f349febc74.png)

<a name="menu"> </a>

<h2> File menu </h2>

<h3> Menu </h3>

The menu has similar options in each part of the program to allow the user to either skip ahead in the program in case certain steps aren't needed or go back to other parts in case the user later decided something else was needed. 

This is an example list for the download program:

![Menu example](https://user-images.githubusercontent.com/81875107/140842262-53baa0c0-1455-4b21-96c5-43cfb9b8dcec.png)

<h3> Properties </h3>

Properties contains only one function (more may be added in the future). It allows the theme for all windows to be changed using the preset themes available in PySimpleGUI. This will change the background color of windows, color of text and background for input fields, and button colors.

Here is what pops up when the __properties__ option is selected:

![Properties option](https://user-images.githubusercontent.com/81875107/140842277-1e1712f9-e695-4fab-87da-9440e3478692.png)

A preview window opens showing what the options for an input field, a button, and the background will look like:

![Properties option showing potential change](https://user-images.githubusercontent.com/81875107/141378935-0a5b45f0-0721-4b27-93c7-c0cae8c7bbda.png)

Selecting __OK__ causes the following popup to appear, alerting the user to the theme chosen:

![Theme changed](https://user-images.githubusercontent.com/81875107/140842324-6fb54fc0-5b93-4777-a9e7-57feb9ed01e0.png)

Which then refreshes the current window that properties was selected from, showing the new theme:

![Window after theme change](https://user-images.githubusercontent.com/81875107/140842339-d96dd395-7c6f-4748-8f8d-b90a87fb26e7.png)

This theme is written into a .json file that the program will read from at the start and remember for future iterations of the program!

This concludes the walkthrough for this program!
