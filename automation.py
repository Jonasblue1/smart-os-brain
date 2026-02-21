import subprocess
from logger import log


def run_task(command):
    try:
        subprocess.Popen(command, shell=True)
        log(f"Executed: {command}")
    except Exception as e:
        log(f"Failed: {e}")
