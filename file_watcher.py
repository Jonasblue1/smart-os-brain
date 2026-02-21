import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from hash_scanner import compute_sha256, MALWARE_HASHES
from logger import log

# Only monitor these extensions
MONITORED_EXTENSIONS = {".exe", ".dll", ".bat", ".ps1", ".vbs", ".js", ".scr"}


class WatcherHandler(FileSystemEventHandler):

    def on_created(self, event):
        if event.is_directory:
            return

        file_path = event.src_path
        _, ext = os.path.splitext(file_path)

        if ext.lower() not in MONITORED_EXTENSIONS:
            return

        log(f"[FILE WATCHER] New file detected: {file_path}")

        file_hash = compute_sha256(file_path)

        if file_hash and file_hash in MALWARE_HASHES:
            log(f"[REAL-TIME ALERT] Malware detected: {file_path}")
        else:
            log(f"[FILE WATCHER] File scanned clean: {file_path}")


def start_file_watcher(directory):
    log(f"[FILE WATCHER] Monitoring: {directory}")

    event_handler = WatcherHandler()
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
