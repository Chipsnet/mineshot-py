import os
import time
import tkinter
import threading
from tkinter import filedialog


def set_dir():
    print('system: Open directory dialog')

    new_dir = filedialog.askdirectory(initialdir = first_dir)
    
    print('new_dir: {}'.format(new_dir))

    dir_box.delete(0, tkinter.END)
    dir_box.insert(tkinter.END,new_dir)

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from PythonMagick import Image

class ChangeHandler(FileSystemEventHandler):
    def on_created(self, event):
        filepath = event.src_path
        filename = os.path.basename(filepath)
        
        print('newfile: '+filepath)
        
        time.sleep(1)
        Image(filepath).write("clipboard:") 

class startSerch(threading.Thread):
    def __init__(self, target_dir):
        super(startSerch, self).__init__()
        self.stop_event = threading.Event()
        self.dir = target_dir

    def stop(self):
        self.stop_event.set()


    def run(self):
        print('system: Process started.')

        target_dir = self.dir

        print('target_dir: {}'.format(target_dir))

        while not self.stop_event.is_set():
            event_handler = ChangeHandler()
            observer = Observer()
            observer.schedule(event_handler, target_dir, recursive=True)
            
            observer.start()
            
            try:
                while not self.stop_event.is_set():
                    time.sleep(0.1)
            except KeyboardInterrupt:
                observer.stop()
            
            print('system: Process ended.')
            observer.stop()


def start():
    print('system: Start button pushed.')

    global target_dir
    global th

    target_dir = dir_box.get()

    th = startSerch(target_dir)
    th.setDaemon(True)
    th.start()

    start_btn["state"] = "disable"
    stop_btn["state"] = "active"


def stop(th):
    print('system: Stop button pushed.')

    th.stop()

    stop_btn["state"] = "disable"
    start_btn["state"] = "active"

th = ''
target_dir = ''

root = tkinter.Tk()

print('system: Loading window data...')

root.title(u'Mineshot v2.0')
root.geometry('500x300')

appdata = os.getenv('APPDATA')
first_dir = '{}\.minecraft\screenshots'.format(appdata)

lbl = tkinter.Label(text='監視対象フォルダ')
lbl.place(x=90, y=70)

dir_box = tkinter.Entry(width=50)
dir_box.place(x=90, y=90)
dir_box.insert(tkinter.END,first_dir)

dir_btn = tkinter.Button(root, text='フォルダの参照', command=set_dir)
dir_btn.place(x=90, y=110)

start_btn = tkinter.Button(root, text='監視スタート', command=start)
start_btn.place(x=90, y=160)

stop_btn = tkinter.Button(root, text='監視ストップ', command=lambda:stop(th))
stop_btn.place(x=170, y=160)
stop_btn["state"] = "disable"

print('system: Window loading completed.')

root.mainloop()