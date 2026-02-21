import threading
import uvicorn

from security_monitor import SecurityMonitor
from ai_anomaly import start_ai_monitor
from file_watcher import start_file_watcher
from ransomware_detector import start_ransomware_monitor
from network_monitor import start_network_monitor


def start_api():
    uvicorn.run("api_server:app", host="127.0.0.1", port=8010, reload=False)


def main():
    print("SMART OS BRAIN BACKEND STARTING")

    SecurityMonitor().start()

    threading.Thread(target=start_ai_monitor, daemon=True).start()
    threading.Thread(
        target=start_file_watcher,
        args=(r"C:\Users\HP\Downloads",),
        daemon=True
    ).start()
    threading.Thread(target=start_ransomware_monitor, daemon=True).start()
    threading.Thread(target=start_network_monitor, daemon=True).start()

    start_api()


if __name__ == "__main__":
    main()
