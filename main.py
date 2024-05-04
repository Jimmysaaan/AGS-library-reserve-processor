import time
from time import sleep
from pynput import keyboard
from pynput.keyboard import Key, Controller

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
    if timeout_result == False:
        result = windll.user32.MessageBoxExW(None,"Reserve dialog box not detected.\nDo you want to continue anyway?","AGS Library reserve processor",ICON_INFO|MB_YESNO)
        print("timed out",result)
        if result == 7:
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
        windll.user32.MessageBoxExW(None,"Time out while waiting for Print dialog box.", "AGS Library reserve processor",ICON_STOP)
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
        windll.user32.MessageBoxExW(None,"Time out while waiting for  email sent confirmation dialog box.", "AGS Library reserve processor",ICON_STOP)
        print("timed out")
        return
    sleep(20/1000)
    k.press(Key.enter)

def stop_thread():
    exit()


with keyboard.GlobalHotKeys(
    {
        "<Shift>+<Alt>+r": run_reserve_process,
        "<Ctrl>+c": stop_thread,
    }
) as h:
    h.join()
