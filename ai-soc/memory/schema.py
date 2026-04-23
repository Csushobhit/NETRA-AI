from memory.normalizer import normalize

def build_record(ip, feature, decision, risk, feedback=None):
    return {
        "ip": ip,
        "feature_vector": normalize(feature),
        "request_freq": feature["request_freq"],
        "failed_ratio": feature["failed_ratio"],
        "unique_ports": feature["unique_ports"],
        "off_hour": feature["off_hour"],
        "decision": decision,
        "risk": risk,
        "feedback": feedback or "unknown"
    }