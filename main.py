import threading
import time
from time import sleep

from pynput import keyboard
from pynput.keyboard import Key, Controller

import gui
from ctypes import wintypes, windll, create_unicode_buffer

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

def getForegroundWindowTitle() :
    hWnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hWnd)
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hWnd, buf, length + 1)

    return buf.value if buf.value else None

def activeWindowIs(window_title: str):
    return getForegroundWindowTitle() == window_title

def timeout_a_function(function, args, timeout_duration):
    #timeout_duration is in seconds
    start = time.process_time()
    while True:
        if time.process_time() - start > timeout_duration:
            return None
        value =  function(*args)
        if value:
            return value

k = Controller()
def run_reserve_process():
    #entry detection
    print("ran")
    timeout_result = activeWindowIs("Select Option")
    if not timeout_result:
        m.signal(0)
        while (result := m.consume_result()) is None:
            pass
        print("timed out",result)
        if result != 6: #6 is the success (continue) result of the msg box
            return
    sleep(20/1000)
    k.press(Key.tab)
    sleep(20/1000)
    k.press(Key.tab)
    sleep(20/1000)
    k.press(Key.space)
    for _ in range(2):
        sleep(20/1000)
        k.press(Key.tab)
        sleep(20/1000)
        k.press(Key.space)
    k.press(Key.enter)
    #time out sequence
    timeout_result = timeout_a_function(activeWindowIs,("Print",),3)
    if timeout_result is None:
        m.signal(1)
        print("timed out")
        return
    k.press(Key.enter)
    #exits time out sequence
    sleep(20/1000)
    k.press(Key.enter)
    sleep(20/1000)
    for _ in range(3):
        k.press(Key.tab)
    sleep(20/1000)
    k.press(Key.enter)
    #time out sequence
    timeout_result = timeout_a_function(activeWindowIs,("Confirmation",),3)
    if timeout_result is None:
        m.signal(2)
        print("timed out")
        return
    sleep(20/1000)
    k.press(Key.enter)

def stop_thread():
    m.signal(-1)
    exit()

m = gui.MsgBoxManager()
m.add_msg_box_attributes(None,"Reserve dialog box not detected.\nDo you want to continue anyway?","AGS Library reserve processor",ICON_INFO|MB_YESNO)
m.add_msg_box_attributes(None,"Time out while waiting for Print dialog box.", "AGS Library reserve processor",ICON_STOP)
m.add_msg_box_attributes(None,"Time out while waiting for  email sent confirmation dialog box.", "AGS Library reserve processor",ICON_STOP)
m.start()

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
        "<Shift>+<Alt>+r": __hotkey__,
        "<Ctrl>+c": stop_thread,
    }
) as h:
    h.join()
