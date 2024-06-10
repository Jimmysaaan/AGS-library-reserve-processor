/*
Library reserve processor v0.5.0-beta-AHK

Copyright 2024 George Gong, Jimson Cui

About this script:
This script automates the reserving process of the AGS library, which uses Accessit software.
Press 'alt+r' to run this script to process a reserve.
This script checks the requires checkboxes in the reserve dialog box to:
-	Print letter
-	Print receipt
-	Send email
The script then proceeds to press OK on subsequent dialog boxes.
*/

#Requires AutoHotkey v2.0 
#SingleInstance Force

;Configuring how `Send` sends out keys
SendMode "Event" ;makes Send synonymous with SendEvent instead of SendInput (allows SetKeyDelay to work)
SetKeyDelay 20 ;20ms of delay between keypresses

A_TrayMenu.Delete() ;clears tray menu 
A_TrayMenu.Add("&About", about) ;adds "About" button and calls "about" when clicked
A_TrayMenu.Add() ;adds a separator
A_TrayMenu.AddStandard() ;adds default tray menu items including "Suspend Hotkeys" and "Exit"

about(*){ ;shows the about box
	;AutoGUI 2.5.8 creator: Alguimist autohotkey.com/boards/viewtopic.php?f=64&t=89901
	;AHKv2converter creator: github.com/mmikeww/AHK-v2-script-converter
	;Easy_AutoGUI_for_AHKv2 github.com/samfisherirl/Easy-Auto-GUI-for-AHK-v2

	aboutGui := Gui()
	aboutGui.Add("Button", "x10 y266", "&Open GitHub").OnEvent("Click", moreInfo)
	aboutGui.Opt("-MinimizeBox -MaximizeBox")
	aboutGui.SetFont("s20 cNavy")
	aboutGui.Add("Text", "x10 y10 w310 h30 +0x200", "Library reserve processor")
	aboutGui.SetFont("s8 Norm cBlack", "Ms Shell Dlg")
	
	aboutGui.Add("Text", "x10 y45", "version 0.5.0-beta-AHK") ;**change version number here**
	
	aboutGui.Add("Text", "x327 y270", "© 2024 George Gong, Jimson Cui") ;copyright information
	aboutGui.SetFont("s10 Norm cBlack", "Ms Shell Dlg")
	aboutGui.Add("Text", "x10 y75 w480", "About this script:`nThis script automates the reserving process of the AGS library, which uses Accessit software.`nPress 'alt+r' to run this script to process a reserve.`nThis script checks the requires checkboxes in the reserve dialog box to:`n-`tPrint letter`n-`tPrint receipt`n-`tSend email`nThe script then proceeds to press OK on subsequent dialog boxes.")
	aboutGui.SetFont("s40", "Segoe MDL2 Assets")
	aboutGui.Add("Text", "x436 y10 w50 h50 +0x200", "") ;receipt printer icon from Segoe MDL2 Assets
	aboutGui.OnEvent('Escape', (*) => aboutGui.Destroy())
	aboutGui.Title := "About"
	aboutGui.Show("w500 h300")

	moreInfo(*){
		Run("https://github.com/Jimmysaaan/AGS-library-reserve-processor") ;directs to the GitHub page
	}
}

Hotkey "!r", Action

Action(*){
	OnMessage(WM_HELP := 0x0053, (*) => Run("https://github.com/Jimmysaaan/AGS-library-reserve-processor"))
	g := Gui("+OwnDialogs")
	timeout := WinActive("Select Option") ;Check if the Reserve dialog box is active
	if timeout = 0{
		cont := MsgBox("Reserve dialog box not detected.`nDo you want to continue anyway?", "AGS Library reserve processor", "iconi YN Default2 16384")
		if (cont = "No")
    		return
	}
	send "{Tab 2}{Space}{Tab}{Space}{Tab}{Space}{Enter}" ;selects required checkboxes
	timeout := WinWaitActive("Print", , 3) ;waits for print dialog, 3secs till timeout
	if timeout = 0{
		MsgBox("Time out while waiting for Print dialog box.`n(Error code: 1)", "AGS Library reserve processor", "iconx 16384")
		return
	}
	send "{Enter Up}{Enter}" ;hits enter on the print dialog. `{Enter Up}` is added to apply the SetKeyDelay delay before the keypress
	timeout := WinWaitActive("Confirmation", , 1) ;waits for print confirmation message
	if timeout = 0{
		MsgBox("Time out while waiting for print confirmation dialog box.`n(Error code: 2)", "AGS Library reserve processor", "iconx 16384")
		return
	}
	send "{Enter Up}{Enter}"
	timeout := WinWaitActive("Processing letters...", , 1) ;waits for "processing letters" menu to be foreground window
	if timeout = 0{
		MsgBox('Time out while waiting for "Processing letters..." menu`n(Error code: 3)', "AGS Library reserve processor", "iconx 16384")
		return
	}
	Send "{Enter Up}{Tab 3}{Enter}" ;presses "OK"
	timeout := WinWaitActive("Confirmation", , 5) ;waits for email sent confirmation message
	if timeout = 0{
		MsgBox("Time out while waiting for email sent confirmation dialog box.", "AGS Library reserve processor", "iconx 16384")
		return
	}
	send "{Enter Up}{Enter}" ;hits "OK" on confirmation message
}
