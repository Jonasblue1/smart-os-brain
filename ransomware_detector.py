import time
import psutil
from logger import log
from threat_engine import threat_engine

WRITE_THRESHOLD = 5000000  # safer realistic threshold


def start_ransomware_monitor():
    log("[RANSOMWARE] Monitor started")

    while True:
        for proc in psutil.process_iter(['pid', 'name', 'io_counters']):
            try:
                io = proc.info['io_counters']
                if not io:
                    continue

                if io.write_bytes > WRITE_THRESHOLD:
                    threat_engine.add_event(
                        "RansomwareDetector",
                        40,
                        f"High disk write activity: {proc.info['name']}"
                    )

            except:
                continue

        time.sleep(5)
