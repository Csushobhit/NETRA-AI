import time

from ingestion.reader import read_new_logs
from ingestion.tracker import TimeTracker
from features.feature_engineer import FeatureEngineer
from ml.model import load_model
from ml.inference import get_anomaly_scores
from agents.orchestrator import run_agents
from memory.store import update_feedback


MODEL_PATH = "models/isolation_forest.pkl"

tracker = TimeTracker()
fe = FeatureEngineer()

model = load_model(MODEL_PATH)

print("System started...")

while True:
    logs, ts = read_new_logs(tracker.get())
    tracker.update(ts)

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

        for f, s in zip(features[-3:], scores[-3:]):
            result = run_agents(f, s)

            print("\n------------------------")
            print("IP:", f["ip"])
            print("Score:", round(s, 3))
            print("Attack:", result["attack_type"])
            print("Risk:", result["risk_score"])
            print("Action:", result["action"])
            print("Explanation:", result["explanation"])

            user_feedback = input("Feedback (correct/incorrect/skip): ").strip().lower()

            if user_feedback in ["correct", "incorrect"]:
                update_feedback(f["ip"], user_feedback)

    time.sleep(3)