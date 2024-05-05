import threading
from ctypes import  windll

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

    def signal(self,id_attr:int):
        self.state = id_attr
        self.event.set()

    def consume_result(self):
        if len(self.results) == 0:
            return None
        return self.results.pop(0)