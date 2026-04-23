def get_anomaly_scores(model, data):
    scores = model.decision_function(data)
    return scores