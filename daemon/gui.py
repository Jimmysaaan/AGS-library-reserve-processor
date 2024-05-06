import threading
from ctypes import  windll, create_unicode_buffer


def getForegroundWindowTitle() :
    hWnd = windll.user32.GetForegroundWindow()
    length = windll.user32.GetWindowTextLengthW(hWnd)
    buf = create_unicode_buffer(length + 1)
    windll.user32.GetWindowTextW(hWnd, buf, length + 1)
    return buf.value if buf.value else None

def activeWindowIs(window_title: str):
    return getForegroundWindowTitle() == window_title

class MsgBoxManager():
    def __init__(self) -> None:
        self.msg_boxes = []
        self.state = -1
        self.event = threading.Event()
        self.results = []

    def event_loop(self,event: threading.Event):
        while True:
            event.wait()
            if self.state == -1:
                break
            result = windll.user32.MessageBoxExW(*self.msg_boxes[self.state])
            print(result)
            self.results.append(result)
            event.clear()

    def start(self):
        t = threading.Thread(target=self.event_loop,args=(self.event,))
        t.start()
            
    def add_msg_box_attributes(self,*args):
        self.msg_boxes.append(args)

    def spawn_msgbox(self,id_attr:int):
        self.state = id_attr
        self.event.set()

    def consume_result(self):
        if len(self.results) == 0:
            return None
        return self.results.pop(0)