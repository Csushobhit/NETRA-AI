import json
from config.llm_config import get_llm
from agents.prompts import DECISION_PROMPT

llm = get_llm()


def decide(attack_type, score, memory):
    memory_text = ""

    if memory:
        memory_text = "\n".join([
            f"- risk: {m['risk']}, decision: {m['decision']}, feedback: {m['feedback']}"
            for m in memory
        ])
    else:
        memory_text = "No similar past cases"

    prompt = DECISION_PROMPT.format(
        attack_type=attack_type,
        score=score,
        memory=memory_text
    )

    response = llm.invoke(prompt).content

    return json.loads(response)