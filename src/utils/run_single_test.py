import json
from src.agents.user_proxy import user_proxy
from src.agents.researcher_agent import researcher
from src.agents.evaluator_agent import evaluator


def run_stock_scraper(url: str):
    task_prompt = (
        f"Extract the stock price from this webpage:\n{url}\n"
        "Use the get_stock_price tool."
    )

    researcher_result = user_proxy.initiate_chat(
        researcher,
        message=task_prompt,
        summary_method="last_msg"
    )
    researcher_output = researcher_result.summary


    evaluator_prompt = (
        "You are evaluating the Researcher's stock price extraction.\n\n"
        f"User request:\n{task_prompt}\n\n"
        f"Researcher output:\n{researcher_output}\n\n"
        "Return JSON only."
    )
    evaluator_result = user_proxy.initiate_chat(
        evaluator,
        message=evaluator_prompt,
        summary_method="last_msg"
    )

    try:
        evaluator_json = json.loads(evaluator_result.summary)
    except:
        evaluator_json = {
            "evaluation": "FAILURE",
            "reason": "Evaluator returned invalid JSON",
            "is_valid_price": False
        }

    return {
        "researcher_output": researcher_output,
        "evaluator_output": evaluator_json
    }
