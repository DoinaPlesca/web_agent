from autogen import AssistantAgent
from config import LLM_CONFIG

reflection_agent = AssistantAgent(
    name="reflection_agent",
    llm_config=LLM_CONFIG,
    system_message=(
        "You are a Reflection Agent.\n"
        "Your ONLY task is to produce a single, short critique of the Researcher's JSON.\n\n"

        "Evaluate only:\n"
        "- Is 'stock_price' numeric (int or float)?\n"
        "- Are the JSON keys correct?\n"
        "- Does the 'source' look like a valid URL?\n\n"

        "STRICT RULES:\n"
        "- If the price is numeric, say: 'Price is numeric.'\n"
        "- If the price is NOT numeric, say: 'Price is not numeric.'\n"
        "- Add 1–2 comments about structure and keys.\n"
        "- DO NOT output JSON.\n"
        "- DO NOT repeat or continue after one message.\n"
        "- Output ONLY one short critique.\n"
        "- END your message with EXACTLY: TERMINATE"
    )
)
