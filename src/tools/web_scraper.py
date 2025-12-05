import requests
from bs4 import BeautifulSoup
import time


CACHE = {} # store cached result
CACHE_TTL = 300 #chache valid for 5 min



def get_stock_price(url: str) -> dict:
    """Scrapes stock price with caching and TTL expiration."""

    # check if URL is cached and  is still valid
    current_time = time.time()
    if url in CACHE:
        cached_entry = CACHE[url]
        age = current_time - cached_entry["timestamp"]

        if age < CACHE_TTL:
            # Cache hit (valid)
            return {
                "success": True,
                "price": cached_entry["price"],
                "source_url": url,
                "cached": True
            }
    # validate url
    try:
        if "/quote/" not in url:
            return {"success": False, "error": "Invalid URL. Not a stock quote page."}

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0 Safari/537.36"
            )
        }

        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        price_tag = soup.select_one('fin-streamer[data-field="regularMarketPrice"]')

        if not price_tag:
            return {"success": False, "error": "Price not found"}

        price = float(price_tag.text.replace(",", ""))

        # store in cache
        CACHE[url] = {
            "price": price,
            "timestamp": current_time
        }

        return {
            "success": True,
            "price": price,
            "source_url": url,
            "cached": False
        }

    except Exception as e:
        return {"success": False, "error": str(e)}
