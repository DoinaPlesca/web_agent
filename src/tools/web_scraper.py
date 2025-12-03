import requests
from bs4 import BeautifulSoup

def get_stock_price(url: str) -> dict:
    """
    Extracts stock price from Yahoo Finance (stable and reliable).
    """

    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0 Safari/537.36"
            )
        }

        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        # Yahoo's consistent selector for stock price
        price_tag = soup.select_one('fin-streamer[data-field="regularMarketPrice"]')

        if not price_tag:
            return {"success": False, "error": "Price not found"}

        return {
            "success": True,
            "price": price_tag.text.strip(),
            "source_url": url
        }

    except Exception as e:
        return {"success": False, "error": str(e)}
