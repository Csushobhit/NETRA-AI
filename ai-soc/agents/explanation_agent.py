from langchain_openai import ChatOpenAI
from agents.prompts import EXPLANATION_PROMPT
from config.llm_config import get_llm

llm = get_llm()

def explain(attack_type, reasoning, risk):
    prompt = EXPLANATION_PROMPT.format(
        attack_type=attack_type,
        reasoning=reasoning,
        risk=risk
    )

    return llm.invoke(prompt).content