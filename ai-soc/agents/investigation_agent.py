from config.llm_config import get_llm
from agents.prompts import INVESTIGATION_PROMPT

llm = get_llm()

def investigate(feature, score, memory=None):
    memory_text = ""

    if memory:
        memory_text = "\nPast similar cases:\n"
        for m in memory:
            memory_text += (
                f"- freq={m['request_freq']}, "
                f"failed={m['failed_ratio']}, "
                f"ports={m['unique_ports']}, "
                f"decision={m['decision']}, "
                f"risk={m['risk']}\n"
            )

    prompt = INVESTIGATION_PROMPT.format(
        request_freq=feature["request_freq"],
        failed_ratio=feature["failed_ratio"],
        unique_ports=feature["unique_ports"],
        off_hour=feature["off_hour"],
        score=score
    ) + memory_text

    response = llm.invoke(prompt).content

    import json
    return json.loads(response)