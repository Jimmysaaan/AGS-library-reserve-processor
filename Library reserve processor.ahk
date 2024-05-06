/*
Library reserve processor v0.4.0-beta

Copyright 2024 George Gong, Jimson Cui

About this script:
This script automates the reserving process of the AGS library, which uses Accessit software.
Press 'alt+r' to run this script to process a reserve.
This script checks the requires checkboxes in the reserve dialog box to:
-	Print letter
-	Print receipt
-	Send email
The script then proceeds to press OK on subsequent dialog boxes
*/
#Requires AutoHotkey v2.0 
#SingleInstance Force
!r::
{
	Action()
}

Action(){
	OnMessage(WM_HELP := 0x0053, (*) => Run("https://github.com/Jimmysaaan/AGS-library-reserve-processor"))
	g := Gui("+OwnDialogs")
	timeout := WinActive("Select Option") ;Check if the Reserve dialog box is active
	if timeout = 0{
		cont := MsgBox("Reserve dialog box not detected.`nDo you want to continue anyway?", "AGS Library reserve processor", "iconi YN Default2 16384")
		if (cont = "No")
    		return
	}
	sleep 20
	send "{Tab}"
	sleep 20
	send "{Tab}"
	sleep 20
	send "{Space}" ;selects the first checkbox
	Loop 2{ ;selects the 2 other checkboxes
		sleep 20
		send "{Tab}"
		sleep 20
		send "{Space}"
	}
	send "{Enter}" ;selects "Process"
	timeout := WinWaitActive("Print", , 3) ;Wait for print dialog, 3secs till timeout
	if timeout = 0{
		MsgBox("Time out while waiting for Print dialog box.", "AGS Library reserve processor", "iconx 16384")
		return
	}
	send "{Enter}" ;Hits enter on the print dialog
	timeout := WinWaitActive("Confirmation", , 1) ;waits for print confirmation message
	if timeout = 0{
		MsgBox("Time out while waiting for print confirmation dialog box.", "AGS Library reserve processor", "iconx 16384")
		return
	}
	send "{Enter}"
	sleep 20
	send "{Tab 3}" ;selects "OK" on email dialog box
	sleep 20
	send "{Enter}" ;presses "OK"
	timeout := WinWaitActive("Confirmation", , 5) ;waits for email sent confirmation message
	if timeout = 0{
		MsgBox("Time out while waiting for email sent confirmation dialog box.", "AGS Library reserve processor", "iconx 16384")
		return
	}
	sleep 20
	send "{Enter}" ;hits "OK" on confirmation message
}