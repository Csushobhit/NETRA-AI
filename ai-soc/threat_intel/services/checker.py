from threat_intel.db.queries import exists, store
from threat_intel.services.scorer import get_scores
from threat_intel.services.ti_input_builder import build_ti_input
from agents.ti_agent import run_ti_agent


def classify(ip):
    if exists("maltrail_ips", ip):
        return "malicious", "maltrail"

    if exists("known_malicious_ips", ip):
        return "malicious", "cache"

    if exists("known_risky_ips", ip):
        return "high_risky", "cache"

    if exists("known_low_risky_ips", ip):
        return "low_risky", "cache"

    if exists("known_unknown_ips", ip):
        return "unknown", "cache"

    abuse, otx, vt = get_scores(ip)

    data = build_ti_input(
        ip,
        False,
        None,
        abuse,
        otx,
        vt
    )
    print("TI INPUT:", {
        "ip": ip,
        "abuse": abuse,
        "otx": otx,
        "vt": vt
    })

    result = run_ti_agent(data)

    label = result.get("label", "unknown")

    if label == "malicious":
        store("known_malicious_ips", ip, abuse, "api")

    elif label == "high_risky":
        store("known_risky_ips", ip, abuse, "api")

    elif label == "low_risky":
        store("known_low_risky_ips", ip, abuse, "api")

    else:
        store("known_unknown_ips", ip, abuse, "api")

    return label, "api"