import psutil
import time
from threat_engine import threat_engine
from logger import log

def start_network_monitor():
    log("[NETWORK] Monitor started")

    while True:
        connections = psutil.net_connections(kind='inet')

        for conn in connections:
            if conn.raddr:
                threat_engine.add_event(
                    "NetworkMonitor",
                    2,
                    f"Connection to {conn.raddr.ip}:{conn.raddr.port}"
                )

        time.sleep(15)
