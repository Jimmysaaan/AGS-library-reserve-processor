import f_opt
from configurations import Configurations
from gui import MsgBoxManager
from action import reserve_process

import threading

from pynput import keyboard

MB_OK = 0x0
MB_OKCXL = 0x01
MB_YESNOCXL = 0x03
MB_YESNO = 0x04
MB_HELP = 0x4000
WS_EX_TOPMOST = 0x40000
# icons
ICON_EXCLAIM = 0x30
ICON_INFO = 0x40
ICON_STOP = 0x10

def __hotkey__():
    names = [t.name for t in threading.enumerate()]
    if "temp_process" in names:
        print("reserve process thread already running")
        return
    temp = threading.Thread(target=rp.run_reserve_process)
    temp.name = "temp_process"
    temp.start()

def stop_thread():
    m.spawn_msgbox(-1)
    exit()

c = Configurations()
f_opt.f_opt({
    "-k":([str],c.set_key_binding),
    "-detector":([str],c.set_reserve_menu_detector_behavior)
})
if c.hotkey == "":
    raise ValueError("Hotkey not defined")

m = MsgBoxManager()
m.add_msg_box_attributes(None,"Reserve dialog box not detected.\nDo you want to continue anyway?","AGS Library reserve processor",ICON_INFO|MB_YESNO)
m.add_msg_box_attributes(None,"Time out while waiting for Print dialog box.", "AGS Library reserve processor",ICON_STOP)
m.add_msg_box_attributes(None,"Time out while waiting for  email sent confirmation dialog box.", "AGS Library reserve processor",ICON_STOP)

rp = reserve_process(m,c)

with keyboard.GlobalHotKeys(
    {
        c.hotkey: __hotkey__,
        "<Ctrl>+c": stop_thread,
    }
) as h:
    m.start()
    h.join()
