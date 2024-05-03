# from pywinauto import keyboard as K
from time import sleep
from pynput import keyboard
from pynput.keyboard import Key, Controller
k = Controller()
def run_reserve_process():
    #entry detection
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
