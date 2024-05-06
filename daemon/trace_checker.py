from pynput.keyboard import Listener, Key
import time
import threading
from datetime import timedelta

class ingest_times():
    def __init__(self) -> None:
        self.results = []
        self.lock = threading.Lock()
        self.threads = []
    def append_data(self,data):
        self.lock.acquire()
        self.results.append(data)
        self.lock.release()

    def add(self,data):
        t = threading.Thread(target=self.append_data,args=(data,))
        self.threads.append(t)
        t.start()

    def print_formatted_results(self):
        time_diff = timedelta(seconds=0)
        print(time_diff,self.results[0][1],self.results[0][2])
        for i in range(1,len(self.results)):
            time_diff = timedelta(seconds=self.results[i][0]-self.results[i-1][0])
            print(time_diff,self.results[i][1],self.results[i][2])

def on_press(key):
    curr_time = time.perf_counter()
    data_manager.add((curr_time,key,"pressed"))

def on_release(key):
    curr_time = time.perf_counter()
    if key == Key.esc:
        return False
    data_manager.add((curr_time,key,"released"))

data_manager = ingest_times()
with Listener(on_press=on_press,on_release=on_release) as l:
    l.join()

for thread in data_manager.threads:
    thread.join()
data_manager.print_formatted_results()