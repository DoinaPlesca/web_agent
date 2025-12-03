from autogen import register_function
from src.tools.web_scraper import get_stock_price
from src.agents.researcher_agent import researcher
from src.agents.user_proxy import user_proxy

from src.utils.run_single_test import run_stock_scraper
from src.utils.markdown_export import export_use_cases_to_markdown



register_function(
    get_stock_price,
    caller=researcher,
    executor=user_proxy,
    name="get_stock_price",
    description="Extracts stock price from the given financial webpage."
)


def run_all_test_cases_and_export():

    test_urls = [
        "https://www.google.com/finance/quote/META:NASDAQ",
        "https://www.google.com/finance/quote/AAPL:NASDAQ",
        "https://www.google.com/finance/quote/GOOG:NASDAQ",
        "https://www.google.com/finance/quote/INVALID:NASDAQ",
        "https://www.google.com/finance/"
    ]

    results = []

    for url in test_urls:
        print(f"\nRunning: {url}")
        result = run_stock_scraper(url)
        results.append((url, result))

    export_use_cases_to_markdown(results)
    print("\nAll tests finished.\n")
