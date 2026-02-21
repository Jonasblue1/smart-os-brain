import time
import psutil
from logger import log

CPU_THRESHOLD = 85
MEMORY_THRESHOLD = 800  # MB

WHITELIST = [
    "system idle process",
    "memcompression",
    "svchost.exe",
    "explorer.exe",
    "chatgpt.exe",
    "system"
]


def check_anomalies():
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            name = (proc.info.get('name') or "").lower()

            if not name:
                continue

            # Skip whitelisted processes
            if name in WHITELIST:
                continue

            cpu = proc.cpu_percent(interval=0.1)

            memory_info = proc.info.get('memory_info')
            if not memory_info:
                continue

            memory = memory_info.rss / (1024 * 1024)

            if cpu > CPU_THRESHOLD:
                log(f"[AI ALERT] High CPU usage: {name} ({cpu}%)")

            if memory > MEMORY_THRESHOLD:
                log(f"[AI ALERT] High Memory usage: {name} ({memory:.2f} MB)")

        except (psutil.NoSuchProcess, psutil.AccessDenied, KeyError):
            continue


def start_ai_monitor():
    log("[AI] AI Anomaly Detection Started")

    while True:
        check_anomalies()
        time.sleep(5)
