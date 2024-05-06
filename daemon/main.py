import f_opt
from gui import activeWindowIs, MsgBoxManager
from configurations import Configurations

import threading
import time
from time import sleep

from pynput import keyboard
from pynput.keyboard import Key, Controller

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


def timeout_a_function(function, args, timeout_duration):
    #timeout_duration is in seconds
    start = time.process_time()
    while True:
        if time.process_time() - start > timeout_duration:
            return None
        value =  function(*args)
        if value:
            return value

def press_and_release(key):
    k.press(key)
    k.release(key)

k = Controller()
def run_reserve_process():
    #entry detection
    print("ran")
    timeout_result = activeWindowIs("Select Option")
    if not timeout_result:
        if c.behavior_of_reserve_menu_detector == c.behaviors["DO_NOT_TRIGGER"]:
            return

        m.signal(0)
        while (result := m.consume_result()) is None:
            pass
        print("timed out",result)
        if result != 6: #6 is the success (continue) result of the msg box
            return

    for _ in range(2):
        sleep(20/1000)
        press_and_release(Key.tab)
    sleep(20/1000)
    press_and_release(Key.space)
    for _ in range(2):
        sleep(20/1000)
        press_and_release(Key.tab)
        sleep(20/1000)
        press_and_release(Key.space)
    press_and_release(Key.enter)
    #time out sequence
    timeout_result = timeout_a_function(activeWindowIs,("Print",),3)
    if timeout_result is None:
        m.signal(1)
        print("timed out")
        return
    #exits time out sequence
    for _ in range(2):
        press_and_release(Key.enter)
        sleep(20/1000)
    for _ in range(3):
        press_and_release(Key.tab)
    sleep(20/1000)
    press_and_release(Key.enter)
    #time out sequence
    timeout_result = timeout_a_function(activeWindowIs,("Confirmation",),3)
    if timeout_result is None:
        m.signal(2)
        print("timed out")
        return
    sleep(20/1000)
    press_and_release(Key.enter)

def stop_thread():
    m.signal(-1)
    exit()

c = Configurations()
f_opt.f_opt({
    "-k":([str],c.set_key_binding),
    "-detector":([str],c.set_reserve_menu_detector_behavior)
})

if c.hotkey == "":
    raise ValueError("Hotkey not defined")

def __hotkey__():
    names = [t.name for t in threading.enumerate()]
    if "temp_process" in names:
        print("reserve process thread already running")
        return
    temp = threading.Thread(target=run_reserve_process)
    temp.name = "temp_process"
    temp.start()

with keyboard.GlobalHotKeys(
    {
        c.hotkey: __hotkey__,
        "<Ctrl>+c": stop_thread,
    }
) as h:
    m = MsgBoxManager()
    m.add_msg_box_attributes(None,"Reserve dialog box not detected.\nDo you want to continue anyway?","AGS Library reserve processor",ICON_INFO|MB_YESNO)
    m.add_msg_box_attributes(None,"Time out while waiting for Print dialog box.", "AGS Library reserve processor",ICON_STOP)
    m.add_msg_box_attributes(None,"Time out while waiting for  email sent confirmation dialog box.", "AGS Library reserve processor",ICON_STOP)
    m.start()
    h.join()
