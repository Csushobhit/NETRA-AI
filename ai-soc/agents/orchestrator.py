from agents.investigation_agent import investigate
from agents.decision_agent import decide
from agents.explanation_agent import explain

from memory.retrieve import get_similar
from memory.store import save_record
from memory.schema import build_record

def run_agents(feature, score):
    # Step 0: retrieve memory
    memory = get_similar(feature)

    # Step 1: investigation (pass memory later if needed)
    memory = get_similar(feature)
    inv = investigate(feature, score, memory)

    attack_type = inv["attack_type"]
    reasoning = inv["reasoning"]

    # Step 2: decision
    dec = decide(attack_type, score, memory)

    risk = dec["risk_score"]
    action = dec["action"]

    # Step 3: explanation
    exp = explain(attack_type, reasoning, risk)

    # Step 4: store memory
    record = build_record(feature["ip"], feature, action, risk)
    save_record(record)

    return {
        "attack_type": attack_type,
        "reasoning": reasoning,
        "risk_score": risk,
        "action": action,
        "explanation": exp
    }