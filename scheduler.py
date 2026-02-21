import json
import time
import threading
from datetime import datetime, timedelta
from automation import run_task
from logger import log

TASK_FILE = "tasks/tasks.json"


class Scheduler:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        try:
            with open(TASK_FILE, "r") as f:
                self.tasks = json.load(f)

            for t in self.tasks:
                t["next_run"] = datetime.now()
        except:
            self.tasks = []

    def save_tasks(self):
        clean = [
            {"command": t["command"], "interval": t["interval"]}
            for t in self.tasks
        ]
        with open(TASK_FILE, "w") as f:
            json.dump(clean, f, indent=4)

    def add_task(self, command, interval):
        task = {
            "command": command,
            "interval": int(interval),
            "next_run": datetime.now()
        }
        self.tasks.append(task)
        self.save_tasks()
        log(f"Scheduled: {command}")

    def loop(self):
        while True:
            now = datetime.now()

            for t in self.tasks:
                if now >= t["next_run"]:
                    run_task(t["command"])
                    t["next_run"] = now + timedelta(minutes=t["interval"])

            time.sleep(1)

    def start(self):
        threading.Thread(target=self.loop, daemon=True).start()


scheduler = Scheduler()
