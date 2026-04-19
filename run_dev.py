import subprocess
import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import sys

PROCESS = None

class ReloadHandler(FileSystemEventHandler):
    def on_modified(self, event):
        global PROCESS
        if event.src_path.endswith(".py"):
            print("🔁 Reloading...")
            if PROCESS:
                PROCESS.kill()
            PROCESS = subprocess.Popen([sys.executable, "main.py"])

if __name__ == "__main__":
    event_handler = ReloadHandler()
    observer = Observer()
    observer.schedule(event_handler, path=".", recursive=True)
    observer.start()

    PPROCESS = subprocess.Popen([sys.executable, "main.py"])

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        if PROCESS:
            PROCESS.kill()

    observer.join()