import psutil
import threading
import time
from logger import log
from quarantine import quarantine_process

BAD_NAMES = ["miner", "crypto", "hack", "rat", "keylog", "payload"]

SYSTEM_PROCESS_WHITELIST = [
    "system idle process",
    "system",
    "memcompression",
    "registry",
    "smss.exe",
    "csrss.exe",
    "wininit.exe",
    "services.exe",
    "lsass.exe",
    "svchost.exe",
    "explorer.exe"
]


class SecurityMonitor:
    def __init__(self):
        self.threats = []

    def scan(self):
        log("[SECURITY] Monitor active.")

        while True:
            log("[SECURITY] Scanning processes...")

            for p in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    name = (p.info.get('name') or "").lower()

                    if not name:
                        continue

                    # 🚫 Skip PID 0 and critical system processes
                    if p.pid == 0 or name in SYSTEM_PROCESS_WHITELIST:
                        continue

                    cpu = p.cpu_percent(interval=0.1)

                    suspicious = cpu > 60 or any(b in name for b in BAD_NAMES)

                    if suspicious:
                        alert = {
                            "name": name,
                            "pid": p.pid,
                            "reason": "Rule-based threat",
                            "action": "quarantined"
                        }

                        quarantine_process(p.pid)

                        self.threats.append(alert)
                        log(f"[THREAT DETECTED] {alert}")

                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            time.sleep(5)

    def start(self):
        threading.Thread(target=self.scan, daemon=True).start()


security_monitor = SecurityMonitor()
