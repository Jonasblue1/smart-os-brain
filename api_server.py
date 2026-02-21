from fastapi import FastAPI
from threat_engine import threat_engine
import psutil
import subprocess
import threading
import time

app = FastAPI()

scheduled_tasks = []


@app.get("/stats")
def get_stats():
    return {
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent,
    }


@app.get("/threats")
def get_threats():
    return threat_engine.get_events()


@app.get("/anomalies")
def get_anomalies():
    return threat_engine.get_events()


@app.post("/run")
def run_command(command: str):
    try:
        subprocess.Popen(command, shell=True)
        return {"status": "command executed"}
    except Exception as e:
        return {"error": str(e)}


@app.post("/schedule")
def schedule_command(command: str, interval: int):
    def task():
        while True:
            subprocess.Popen(command, shell=True)
            time.sleep(int(interval) * 60)

    thread = threading.Thread(target=task, daemon=True)
    thread.start()
    scheduled_tasks.append(command)

    return {"status": "scheduled"}
