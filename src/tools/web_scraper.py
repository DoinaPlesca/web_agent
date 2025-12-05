import threading
import requests
from bs4 import BeautifulSoup
import time


CACHE = {} # store cached result
CACHE_TTL = 300 #chache valid for 5 min

MAX_REQUESTS_PER_MINUTE = 10        # Global rate limit
REQUEST_HISTORY = []                # Timestamp list for rate limiting
REQUEST_HISTORY_LOCK = threading.Lock()

MAX_RETRIES = 3                     # Retry attempts for scraping
BACKOFF_BASE = 1                    # Exponential backoff base (1, 2, 4 sec)


def rate_limited():
    """Ensures no more than MAX_REQUESTS_PER_MINUTE run per 60 seconds."""

    now = time.time()
    with REQUEST_HISTORY_LOCK:
        # Remove timestamps older than 60 seconds
        while REQUEST_HISTORY and now - REQUEST_HISTORY[0] > 60:
            REQUEST_HISTORY.pop(0)

        if len(REQUEST_HISTORY) < MAX_REQUESTS_PER_MINUTE:
            REQUEST_HISTORY.append(now)
            return True

        return False


def wait_until_rate_available():
    """Blocks until rate limiting allows execution."""

    while not rate_limited():
        time.sleep(0.2)  # wait 200ms and check again



def get_stock_price(url: str) -> dict:
     """
    Scrapes stock price from Yahoo Finance with:
    - TTL cache
    - global rate limiting
    - retry with exponential backoff
    - fallback to cached value if failure
    """


     now = time.time()

     if url in CACHE:
        cached_entry = CACHE[url]
        age = now - cached_entry["timestamp"]

        if age < CACHE_TTL:
            # Cache hit (valid)
            return {
                "success": True,
                "price": cached_entry["price"],
                "source_url": url,
                "cached": True
            }

    # validate url
     if "/quote/" not in url:
            return {"success": False, "error": "Invalid URL. Not a stock quote page."}

     headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0 Safari/537.36"
        )
     }

     last_exception = None

     for attempt in range(MAX_RETRIES):
         try:
             #  RATE LIMIT
             wait_until_rate_available()

             # SEND REQUEST
             response = requests.get(url, headers=headers, timeout=10)
             soup = BeautifulSoup(response.text, "html.parser")

             # PARSE PRICE
             price_tag = soup.select_one('fin-streamer[data-field="regularMarketPrice"]')

             if not price_tag:
                 last_exception = Exception("Price not found")
                 raise last_exception

             price = float(price_tag.text.replace(",", ""))

             # STORE IN CACHE
             CACHE[url] = {"price": price, "timestamp": now}

             return {
                 "success": True,
                 "price": price,
                 "source_url": url,
                 "cached": False
             }

         except Exception as e:
             last_exception = e

             if attempt < MAX_RETRIES - 1:
                 # exponential backoff
                 delay = BACKOFF_BASE * (2 ** attempt)
                 time.sleep(delay)
             else:
                 break  # final failure → proceed to fallback


     if url in CACHE:
         cached_entry = CACHE[url]
         return {
             "success": True,
             "price": cached_entry["price"],
             "source_url": url,
             "cached": True,
             "warning": "Returned expired cached result due to scraping failure."
         }

     return {
         "success": False,
         "error": f"Scraping failed after retries: {str(last_exception)}"
     }