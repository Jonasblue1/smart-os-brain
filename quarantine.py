import os
import shutil
import psutil
from datetime import datetime
from logger import log

QUARANTINE_DIR = "quarantine"


def quarantine_process(pid):
    try:
        p = psutil.Process(pid)
        path = p.exe()

        if not path or not os.path.exists(path):
            return False

        p.kill()

        filename = os.path.basename(path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        new_name = f"{timestamp}_{filename}"
        new_path = os.path.join(QUARANTINE_DIR, new_name)

        shutil.move(path, new_path)

        log(f"[QUARANTINED] {filename} -> {new_path}")

        return True

    except Exception as e:
        log(f"[QUARANTINE FAILED] {e}")
        return False
