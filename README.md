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

This app interacts with a user's Google Photos and Drive, and as such, will prompt for an account sign in when accessing either the upload or download functions. After one week, the app will request permission again; this is normal as the app is unverified from Google, so tokens only last for 1 week.

<a name="Photodownload"> </a>

<h2> Photo download </h2>

The program begins in this first window:

![Beginning window](https://user-images.githubusercontent.com/81875107/142804179-27ecc156-bc83-4ba1-a020-d9287b1ae7f5.png)

where the user is prompted to enter a folder on the local host to download photos to, and to select from either a single date:

![Single date selection](https://user-images.githubusercontent.com/81875107/142804204-e7ab24d6-d2d9-4c85-be91-874692cdd404.png)

or a date range, where each of the buttons opens a calendar as shown above for each prompt:

![Date range selection](https://user-images.githubusercontent.com/81875107/142804241-c49cfed9-0621-4dab-88c8-01c5b3c100ff.png)

After the user has selected a folder and date(s) the program calls the Google Photos API with the date filter input by the user for all photos in the range. The program then updates the user by showing a progress window for how many photos will be downloaded and how many have currently been downloaded:

![Download with a progress bar](https://user-images.githubusercontent.com/81875107/142804265-3eae0262-fd91-4216-95dc-b9d78af56c3a.png)

<a name="newfoldercreation"> </a>

<h2> New folder creation </h2>

After the user is done using the download tool and selects the correct button, the user is prompted for new inputs:

![Program flow after download](https://user-images.githubusercontent.com/81875107/142804315-ad02df1f-32ef-432b-ae48-5d4780b6932b.png)

Selecting yes for the first radio brings the user to a window as shown below. The user is asked for a location to make new folders, and how many should be created in the new location. If an entry of 0 is received, the program will continue on the flow without prompting to create new folders.

![Folder creation option](https://user-images.githubusercontent.com/81875107/142804336-6560a890-d511-4acd-b875-68a67999fd20.png)

<a name="movingfiles"> </a>

<h2> Moving files </h2>

Here is the window for moving files from one folder to another (for example, moving files from a USB drive to a storage folder on the user's PC):

![File mover example](https://user-images.githubusercontent.com/81875107/142804370-90f38d9b-fc4d-4fa2-a4f4-d799df51c948.png)

The window requires the user to input a source folder and a destination folder. Then the .jpg, .png, .jpeg, and .pdf files are shown in each of the folders. The user can select individual or multiple (using CTRL if needed) files to move to the destination folder. Image files are shown in the middle, while .pdf shows a generic image file. Clicking __Move &#x2192;__ copies the file to the destination folder and then deletes it from the first folder.

![File mover example 2](https://user-images.githubusercontent.com/81875107/142804390-3ce9bc38-4243-4974-8d76-e922041b875f.png)

<a name="renamingfiles"> </a>

<h2> Renaming files </h2>

Renaming files is accomplished in this window:

![File renamer example](https://user-images.githubusercontent.com/81875107/142804414-2a33aa0c-d132-49c1-a68a-6ac3020710de.png)

which updates the file list after a name has been entered:

![File renamed](https://user-images.githubusercontent.com/81875107/142804436-b47d320a-080c-4059-bd1a-927070faa17c.png)

Multiple files can be updated at once using the __Mass rename__ button:

![Mass rename example](https://user-images.githubusercontent.com/81875107/142804456-ed571d02-9fa0-4636-9dae-f17214a8ea2e.png)

which results in files following a format like below:

![After mass rename](https://user-images.githubusercontent.com/81875107/142804479-b49941c2-cae5-4ca1-be3f-718301ec1c75.png)

The delete button does exactly what it says, it deletes the file from the local host. It does not move it to a recycle area, it is gone. Delete has a confirmation before the file is deleted, as shown below:

![Delete confirmation](https://user-images.githubusercontent.com/81875107/142804507-12466e96-9c1d-4ef1-8eb7-afd16662d5da.png)

Which results in the file being removed and the viewer being cleared:

![File deleted](https://user-images.githubusercontent.com/81875107/142804525-d41e772d-e53c-4fa2-9cc5-6ea03a42a82b.png)

The two rotate buttons, Rotate &#x2B6E; and Rotate &#x2B6F;, rotate the image clockwise and counterclockwise 90&#x00B0; in the corresponding direction.

Rotate &#x2B6E;:

![Rotate 90 clockwise](https://user-images.githubusercontent.com/81875107/142804549-0ef172e8-cc6f-423d-8f4c-38cd747a32f1.png)

Rotate &#x2B6F;:

![Rotate 90 counterclockwise](https://user-images.githubusercontent.com/81875107/142804564-aeac4716-d500-4473-8197-d0de08776ede.png)

Upload moves on to the last major part of the program.

<a name ="uploadingfiles"> </a>

<h2> Uploading files </h2>

The program prompts for user input on several areas for upload. Shared flags the files to be visible by other collaborators for shared Drives, and not sharing causes the file(s) to be uploaded to the user's Drive instead. Note that the file renamer portion stays open while the upload program is running so that the user can switch folders to upload more files, if desired.

![File uploader window](https://user-images.githubusercontent.com/81875107/142804593-8bd06b8e-7a8b-4ed2-ab87-589468f1d864.png)

Below shows the windows opened while uploading files. The background window is the list of Drive folders the user can upload to. This list can be shortened to include commonly used folders by editting the .json file that is created when gathering all the folders the first time. Otherwise, the program just uses the full list to help reduce the amount of time it takes to look for Drive folders.

![File uploader windows](https://user-images.githubusercontent.com/81875107/142804621-fffd1d44-5214-4dfc-969c-31985d3ec9e8.png)

<a name="menu"> </a>

<h2> File menu </h2>

<h3> Menu </h3>

The menu has similar options in each part of the program to allow the user to either skip ahead in the program in case certain steps aren't needed or go back to other parts in case the user later decided something else was needed.

This is an example list for the download program:

![Menu example](https://user-images.githubusercontent.com/81875107/142804639-8e595308-83b7-430f-a297-1ed7eabbafed.png)

<h3> Properties </h3>

Properties contains two different functions (more may be added in the future). __Themes__ allows the theme for all windows to be changed using the preset themes available in PySimpleGUI. This will change the background color of windows, color of text and background for input fields, and button colors. The second option, __Image Size__, changes the size of the images shown in the file mover and the file renamer. Currently, there are only 2 options, but a custom scaler might be added in the future. The Image method for a Window in PySimpleGUI can be a bit finicky with what it considers valid "sizes" for an input; it'll accept custom measurements, but it seems to prefer certain values over others regardless of input.

<h4> Themes </h4>
Here is what pops up when the <strong>Themes</strong> option is selected:

![Themes option](https://user-images.githubusercontent.com/81875107/142804796-68b98e2a-5d52-4199-9e2f-777a05ab7a87.png)

A preview window opens showing what the options for an input field, a button, and the background will look like:

![Themes option showing potential change](https://user-images.githubusercontent.com/81875107/142804809-f45292fd-b436-4ff3-89c8-4dcd4220977e.png)

Selecting __OK__ causes the following popup to appear, alerting the user to the theme chosen:

![Theme changed](https://user-images.githubusercontent.com/81875107/142804821-60b33bb8-277a-4597-af96-91b4f6201019.png)

Which then refreshes the current window that properties was selected from, showing the new theme:

![Window after theme change](https://user-images.githubusercontent.com/81875107/142804846-0cbc2956-d7da-45d5-9e6e-0129b48d452d.png)

This theme is written into a .json file that the program will read from at the start and remember for future iterations of the program!

<h4> Image size </h4>
Here is the image size popup:

![Size option selected](https://user-images.githubusercontent.com/81875107/142805351-155fe542-6b04-42ab-aa5f-e80fe3d701c9.png)

Small size results in images appearing in the viewer as this size:

![small size default](https://user-images.githubusercontent.com/81875107/142806745-e31b432b-fe83-4ab1-87c9-56d3c30f94da.png)

And large shows up as:

![large size](https://user-images.githubusercontent.com/81875107/142806762-da66a951-b08c-40c4-b009-687909058c79.png)

Small is the default size, and for the Image method this is equivalent to size = (400, 400). Large is double this at (800, 800). Either option is saved to the same .json as the theme, so future runs will remember any choices made.

This concludes the walkthrough for this program!
