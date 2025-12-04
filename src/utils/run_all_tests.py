import json
from src.utils.run_single_test import run_stock_scraper
from src.utils.markdown_export import export_use_cases_to_markdown

def run_all_test_cases_and_export():

    test_cases = [
        ("Valid stock: META", "https://finance.yahoo.com/quote/META"),
        ("Valid stock: AAPL", "https://finance.yahoo.com/quote/AAPL"),
        ("Valid stock: GOOG", "https://finance.yahoo.com/quote/GOOG"),
        ("Invalid ticker", "https://finance.yahoo.com/quote/INVALID"),
        ("Non-stock homepage", "https://finance.yahoo.com/")
    ]

    results = []

    for name, url in test_cases:
        print(f"Running: {name}")
        result = run_stock_scraper(url)

        try:
            evaluator_json = json.loads(result["evaluator_output"])
        except:
            evaluator_json = {"evaluation": "FAILURE", "reason": "Invalid JSON", "is_valid_price": False}

        results.append({
            "test_name": name,
            "url": url,
            "researcher_output": result["researcher_output"],
            "evaluator_output": evaluator_json
        })

    export_use_cases_to_markdown(results)
    print(" Results exported to use_cases.md")
