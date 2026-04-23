import json
import re
from agents.prompts import TI_PROMPT
from config.llm_config import get_llm

llm = get_llm()

def run_ti_agent(data):
    prompt = TI_PROMPT.format(
        ip=data["ip"],
        maltrail=data["maltrail"],
        cache=data["cache"],
        abuse=data["abuse_score"],
        otx=data["otx_score"],
        vt=data["vt_score"]
    )

    response = llm.invoke(prompt).content

    print("RAW LLM RESPONSE:", response)

    try:
        cleaned = response.strip()

        if cleaned.startswith("```"):
            cleaned = re.sub(r"```json|```", "", cleaned).strip()

        return json.loads(cleaned)

    except:
        match = re.search(r"\{.*\}", response, re.DOTALL)
        if match:
            return json.loads(match.group())

        return {
            "label": "unknown",
            "confidence": 0,
            "reasoning": "Failed to parse agent response"
        }