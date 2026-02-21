from datetime import datetime

def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted = f"[{timestamp}] {message}"

    # Print to console
    print(formatted)

    # Also save to file
    with open("smart_os_log.txt", "a", encoding="utf-8") as f:
        f.write(formatted + "\n")
