
from autogen import AssistantAgent
from config import LLM_CONFIG

evaluator = AssistantAgent(
    name="Evaluator",
    llm_config=LLM_CONFIG,
    system_message=(
        "You are an external evaluator for a stock price extraction agent.\n"
        "You will receive:\n"
        "- the original user request\n"
        "- the Researcher's final JSON output\n\n"
        "Your task is to judge whether the Researcher correctly extracted the stock price.\n\n"
        "Evaluation criteria:\n"
        "- correctness: JSON must contain exactly 'stock_price' (numeric) and 'source' (valid URL)\n"
        "- validity: 'stock_price' must be a real numeric value\n"
        "- formatting: JSON must be well-formed with no extra fields\n\n"
        "Output STRICT JSON ONLY in this format:\n"
        "{\n"
        "  \"evaluation\": \"SUCCESS\" or \"FAILURE\",\n"
        "  \"reason\": \"<brief explanation>\",\n"
        "  \"is_valid_price\": true or false\n"
        "}\n\n"
        "No markdown. No commentary. No surrounding text.\n"
        "Your message MUST end with: TERMINATE"
    )
)
