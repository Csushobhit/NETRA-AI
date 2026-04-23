import joblib
from sklearn.ensemble import IsolationForest

def train_and_save(data, path="model.pkl"):
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(data)
    joblib.dump(model, path)
    return model

def load_model(path="model.pkl"):
    return joblib.load(path)