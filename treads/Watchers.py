import os
from PyQt6.QtCore import QThread, pyqtSignal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class _FileWatcherHandler(FileSystemEventHandler):
    def __init__(self, watch_path, signal):
        super().__init__()
        self.watch_path = os.path.abspath(watch_path)
        self.file_signal = signal
        self.watch_file = os.path.isfile(self.watch_path)

    def on_modified(self, event):
        if event.is_directory:
            return
        
        if self.watch_file:
            if os.path.abspath(event.src_path) == self.watch_path:
                self.file_signal.emit(f"File modified: {event.src_path}")
        else:
            self.file_signal.emit(f"File modified: {event.src_path}")

    def on_created(self, event):
        if not event.is_directory and not self.watch_file:
            self.file_signal.emit(f"File created: {event.src_path}")

    def on_deleted(self, event):
        if not event.is_directory and not self.watch_file:
            self.file_signal.emit(f"File deleted: {event.src_path}")

class WatcherThread(QThread):
    file_signal = pyqtSignal(str)

    def __init__(self, watch_path):
        super().__init__()
        self.watch_path = watch_path
        self.running = True

    def run(self):
        event_handler = _FileWatcherHandler(self.watch_path, self.file_signal)
        observer = Observer()
        watch_dir = os.path.dirname(self.watch_path) if os.path.isfile(self.watch_path) else self.watch_path
        observer.schedule(event_handler, watch_dir, recursive=not os.path.isfile(self.watch_path))
        observer.start()

        try:
            while self.running:
                self.msleep(1000) 
        finally:
            observer.stop()
            observer.join()

    def stop(self):
        self.running = False
        self.quit()
        self.wait()
