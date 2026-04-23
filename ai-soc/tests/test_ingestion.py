import time
from ingestion.reader import read_new_logs
from ingestion.tracker import FileTracker
from features.feature_engineer import FeatureEngineer

tracker = FileTracker()
fe = FeatureEngineer()

while True:
    logs, idx = read_new_logs("logs.csv", tracker.get())
    tracker.update(idx)

    if logs:
        features = fe.process_logs(logs)

        for f in features[-5:]:
            print(f)

    time.sleep(2)