import subprocess
import time
from datetime import datetime, timezone



SERVICE_NAME = "nginx"
CHECK_INTERVAL = 30
LOG_FILE = "watchdog.log"

def log_message(message):
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{timestamp} - {message}"

    print(entry)

    with open(LOG_FILE, "a") as log:
        log.write(entry + "\n")

def is_service_running():
    result = subprocess.run(
        ["systemctl", "is-active", "--quiet", SERVICE_NAME],
        check=False,
    )

    return result.returncode == 0

def start_service():
    log_message(f"{SERVICE_NAME} is stopped. Attempting to start it.")

    result = subprocess.run(
        ["sudo", "systemctl", "start", SERVICE_NAME],
        check=False,
    )

    if result.returncode == 0:
        log_message(f"{SERVICE_NAME} started successfully.")
    else:
        log_message(f"Failed to start {SERVICE_NAME}.")

def watchdog():
    log_message(f"Starting watchdog for {SERVICE_NAME}")

    while True:
        if is_service_running():
            log_message(f"{SERVICE_NAME} is running.")
        else:
            start_service()

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    watchdog()
