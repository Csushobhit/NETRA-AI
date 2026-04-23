import time
import threading
from datetime import datetime

from ingestion.reader import read_new_logs
from ingestion.tracker import TimeTracker
from features.feature_engineer import FeatureEngineer

from api.ml_service import score
from api.agent_service import run
from api.alert_service import store_alert

tracker = TimeTracker()
fe = FeatureEngineer()

def process():
    while True:
        try:
            last_ts = tracker.get()
            logs, new_ts = read_new_logs(last_ts)

            if logs:
                features = fe.process_logs(logs)
                features = score(features)

                for f in features:
                    result = run(f)

                    alert = {
                        "ip": f["ip"],
                        "window": f["window"],
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "request_freq": f["request_freq"],
                        "failed_ratio": f["failed_ratio"],
                        "unique_ports": f["unique_ports"],
                        "off_hour": f["off_hour"],
                        "anomaly_score": f["anomaly_score"],
                        "attack_type": result["attack_type"],
                        "risk_score": result["risk_score"],
                        "action": result["action"],
                        "explanation": result["explanation"]
                    }

                    store_alert(alert)

                tracker.update(new_ts)

        except Exception as e:
            time.sleep(2)
            continue

        time.sleep(2)

def start():
    t = threading.Thread(target=process, daemon=True)
    t.start()