from fastapi import FastAPI
from monitor import get_system_stats
from automation import run_task
from scheduler import scheduler
from security_monitor import security_monitor
from ai_anomaly import ai_detector

app = FastAPI()


@app.get("/stats")
def stats():
    return get_system_stats()


@app.get("/threats")
def threats():
    return security_monitor.threats[-10:]


@app.get("/anomalies")
def anomalies():
    return ai_detector.anomalies[-10:]


@app.post("/run")
def run(command: str):
    run_task(command)
    return {"status": "running"}


@app.post("/schedule")
def schedule(command: str, interval: int):
    scheduler.add_task(command, interval)
    return {"status": "scheduled"}
