from collections import defaultdict
from datetime import datetime

TIME_WINDOW = 60  # seconds

class FeatureEngineer:
    def __init__(self):
        self.state = defaultdict(lambda: {
            "request_count": 0,
            "failed_logins": 0,
            "total_logins": 0,
            "ports": set(),
            "off_hour": 0
        })

    def _get_window(self, timestamp):
        ts = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        return int(ts.timestamp() // TIME_WINDOW), ts.hour

    def process_logs(self, logs):
        results = []

        for log in logs:
            ip = log["ip"]
            window, hour = self._get_window(log["timestamp"])
            key = (ip, window)

            entry = self.state[key]

            # request count
            entry["request_count"] += 1

            # login tracking
            if log["event_type"] == "login":
                entry["total_logins"] += 1
                if log["status"] == "failed":
                    entry["failed_logins"] += 1

            # ports
            entry["ports"].add(int(log["port"]))

            # off-hour (e.g., night)
            if hour < 6 or hour > 23:
                entry["off_hour"] = 1

        # build feature output
        for (ip, window), entry in self.state.items():
            total_logins = entry["total_logins"]

            failed_ratio = (
                entry["failed_logins"] / total_logins
                if total_logins > 0 else 0
            )

            results.append({
                "ip": ip,
                "window": window,
                "request_freq": entry["request_count"],
                "failed_ratio": round(failed_ratio, 2),
                "unique_ports": len(entry["ports"]),
                "off_hour": entry["off_hour"]
            })

        return results