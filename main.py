import json
from pprint import pprint

from src.agents.reflection_agent import reflection_agent
from src.tools.web_scraper import get_stock_price
from src.agents.user_proxy import user_proxy
from src.agents.researcher_agent import researcher
from src.agents.evaluator_agent import evaluator
from autogen import register_function
import warnings
warnings.filterwarnings("ignore")



register_function(
    get_stock_price,
    caller=researcher,
    executor=user_proxy,
    name="get_stock_price",
    description="Extracts stock price from the given financial webpage."
)

def run_stock_scraper(url: str):
    task_prompt = (
        f"Extract the stock price from this webpage:\n{url}\n"
        f"Use the get_stock_price tool."
    )

    chat_result = user_proxy.initiate_chat(
        researcher,
        message=task_prompt,
        summary_method="last_msg"
    )
    researcher_output = chat_result.summary

    """
    reflection_result = user_proxy.initiate_chat(
        reflection_agent,
        message=f"Here is the Researcher's JSON:\n{researcher_output}\n\nProvide critique.",
        summary_method="last_msg"
    )
    reflection_text = reflection_result.summary
    """

    evaluator_result = user_proxy.initiate_chat(
        evaluator,
        message=(
            f"The user asked for: {task_prompt}\n\n"
            f"Researcher output:\n{researcher_output}\n\n"
           #f"Reflection critique:\n{reflection_text}\n\n"
        )
    )
    print("\n--- Evaluation Complete ---\n")


    try:
        evaluation_json = json.loads(evaluator_result.summary)
    except json.JSONDecodeError:
        evaluation_json = {
            "evaluation": "FAILURE",
            "reason": "Evaluator returned invalid JSON.",
            "is_valid_price": False
        }

    pprint(evaluation_json)

    print("\n--- Statistics ---")
    print(f"Task URL: {url}")
    print(f"Success: {evaluation_json.get('evaluation') == 'SUCCESS'}")
    print(f"Failure: {evaluation_json.get('evaluation') == 'FAILURE'}")
    print(f"Valid Price: {evaluation_json.get('is_valid_price')}")
    print(f"Reason: {evaluation_json.get('reason')}")

    return evaluation_json

if __name__ == "__main__":
    run_stock_scraper("https://finance.yahoo.com/quote/META")
