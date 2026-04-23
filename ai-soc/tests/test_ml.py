import time

from ingestion.reader import read_new_logs
from ingestion.tracker import FileTracker
from features.feature_engineer import FeatureEngineer
from ml.model import load_model
from ml.inference import get_anomaly_scores

FILE_PATH = "logs.csv"
MODEL_PATH = "models/isolation_forest.pkl"

tracker = FileTracker()
fe = FeatureEngineer()

# load pre-trained model
model = load_model(MODEL_PATH)
print("Model loaded")

while True:
    logs, idx = read_new_logs(FILE_PATH, tracker.get())
    tracker.update(idx)

    if logs:
        features = fe.process_logs(logs)

        vectors = [
            [
                f["request_freq"],
                f["failed_ratio"],
                f["unique_ports"],
                f["off_hour"]
            ]
            for f in features
        ]

        scores = get_anomaly_scores(model, vectors)

        for f, s in zip(features[-5:], scores[-5:]):
            print(f["ip"], "score:", round(s, 3))

    time.sleep(2)