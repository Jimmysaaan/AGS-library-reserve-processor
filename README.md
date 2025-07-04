![](ec5b.ico)

# AGS library reserve processor
A script to automate the reserving process in the AGS library.

## If something broke...
Make a bug report [here](../../issues/new?template=bug_report.yml).

## About this script
This script automates the reserving process of the AGS library, which uses Accessit software.

Press 'alt+r' to run this script to process a reserve.
This script checks the required checkboxes in the reserve dialog box to:
-	Print letter
-	Print receipt
-	Send email

The script then proceeds to press OK on subsequent dialog boxes.

To stop the script, right click on the tray icon and press `Exit`

## Installation
Download the exe from [releases](../../releases/latest) and run it. It will continue running in the background.

## Compiling
Use [Ahk2Exe](https://www.autohotkey.com/docs/v2/Scripts.htm#ahk2exe) to compile the script. Make sure [`ec5b.ico`](ec5b.ico) is in the same folder as the script.