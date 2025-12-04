
from src.agents.researcher_agent import researcher
from src.agents.evaluator_agent import evaluator
from src.agents.user_proxy import user_proxy

def run_stock_scraper(url: str):

    task_prompt = f"Extract the stock price from this webpage: {url}"


    researcher_result = user_proxy.initiate_chat(
        researcher,
        message=task_prompt,
        summary_method="last_msg"
    )
    researcher_output = researcher_result.summary.strip()


    evaluator_prompt = (
        "Evaluate this JSON:\n"
        f"{researcher_output}"
    )

    evaluator_result = user_proxy.initiate_chat(
        evaluator,
        message=evaluator_prompt,
        summary_method="last_msg"
    )

    evaluator_output = evaluator_result.summary.strip()

    return {
        "researcher_output": researcher_output,
        "evaluator_output": evaluator_output
    }
