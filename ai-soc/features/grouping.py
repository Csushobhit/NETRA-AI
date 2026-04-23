from collections import defaultdict
from datetime import datetime

TIME_WINDOW = 60  # seconds

def group_logs(logs):
    grouped = defaultdict(list)

    for log in logs:
        ip = log["ip"]

        ts = datetime.strptime(log["timestamp"], "%Y-%m-%d %H:%M:%S")
        window = int(ts.timestamp() // TIME_WINDOW)

        key = (ip, window)
        grouped[key].append(log)

    return grouped