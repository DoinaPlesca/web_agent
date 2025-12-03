from datetime import datetime
import json


def export_use_cases_to_markdown(results, filename="use_cases.md"):

    content = []
    content.append("# Web Scraping Agent – Use Case Demonstrations\n")
    content.append("This file was auto-generated.\n")
    content.append(f"Generated on: {datetime.now()}\n")
    content.append("\n---\n")

    for i, (url, result) in enumerate(results, start=1):

        content.append(f"## USE CASE {i}\n")

        content.append("### INPUT\n")
        content.append("```\n")
        content.append(f"Extract the stock price from this webpage:\n{url}\nUse the get_stock_price tool.\n")
        content.append("```\n")

        content.append("### RESEARCHER OUTPUT\n")
        content.append("```\n")
        content.append(result['researcher_output'])
        content.append("\n```\n")

        content.append("### EVALUATOR OUTPUT\n")
        content.append("```\n")
        content.append(json.dumps(result['evaluator_output'], indent=4))
        content.append("\n```\n")

        content.append("\n---\n")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(content))

    print(f"Created {filename}")
