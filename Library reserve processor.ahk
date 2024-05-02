/*
Library reserve processor v0.3.0-alpha

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
!r::
{
	;if it doesnt work, skill issue!
	Action()
}

Action(){
	if WinWaitActive("Select Option", , 1){ ;Wait for Reserve dialog box, 1secs till timeout
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
		if WinWaitActive("Print", , 3){ ;Wait for print dialog, 3secs till timeout
			send "{Enter}" ;Hits enter on the print dialog
		}
		else{
			MsgBox "Time out while waiting for Print dialog box."
			return
		}
		sleep 20
		send "{Enter}"
		sleep 20
		send "{Tab 3}" ;selects "OK" on email dialog box
		sleep 20
		send "{Enter}" ;presses "OK"
		if WinWaitActive("Confirmation", , 3){ ;waits for email sent confirmation message
			sleep 20
			send "{Enter}" ;hits "OK" on confirmation message
		}
		else{
			MsgBox "Time out while waiting for email sent confirmation dialog box."
		}
	}
	else{
		MsgBox "Time out while waiting for 'Select Option' window. Check if the reserve dialog box is open."
	}
}