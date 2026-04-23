from agents.orchestrator import run_agents

def run(feature):
    return run_agents(feature, feature["anomaly_score"])