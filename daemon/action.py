from daemon.configurations import Configurations
from gui import MsgBoxManager, activeWindowIs

import time
from time import sleep
from pynput.keyboard import Key, Controller

k = Controller()
def press_and_release(key):
    k.press(key)
    k.release(key)

def timeout_a_function(function, args, timeout_duration):
    #timeout_duration is in seconds
    start = time.process_time()
    while True:
        if time.process_time() - start > timeout_duration:
            return None
        value =  function(*args)
        if value:
            return value

class reserve_process():
    def __init__(self, msgbox: MsgBoxManager, config: Configurations) -> None:
        self.msgbox =  msgbox
        self.config = config
    def run_reserve_process(self):
        #entry detection
        print("ran")
        timeout_result = activeWindowIs("Select Option")
        if not timeout_result:
            if self.config.behavior_of_reserve_menu_detector == self.config.behaviors["DO_NOT_TRIGGER"]:
                return

            self.msgbox.spawn_msgbox(0)
            while (result := self.msgbox.consume_result()) is None:
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
            self.msgbox.spawn_msgbox(1)
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
            self.msgbox.spawn_msgbox(2)
            print("timed out")
            return
        sleep(20/1000)
        press_and_release(Key.enter)