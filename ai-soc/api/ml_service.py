from ml.model import load_model
from ml.inference import get_anomaly_scores

MODEL_PATH = "models/isolation_forest.pkl"
model = load_model(MODEL_PATH)

def score(features):
    data = []

    for f in features:
        data.append([
            f["request_freq"],
            f["failed_ratio"],
            f["unique_ports"],
            f["off_hour"]
        ])

    scores = get_anomaly_scores(model, data)

    for i in range(len(features)):
        features[i]["anomaly_score"] = float(scores[i])

    return features