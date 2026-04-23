from threat_intel.services.checker import classify
from api.alert_service import update_ti

def run_ti(ip):
    label, source = classify(ip)

    confidence = 80 if label != "unknown" else 0
    reasoning = f"Classified via {source}"

    update_ti(ip, label, confidence, reasoning)

    return {
        "ip": ip,
        "label": label,
        "confidence": confidence,
        "reasoning": reasoning
    }